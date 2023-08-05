import sys
from dataclasses import asdict
from datetime import datetime
from pprint import pprint
from typing import List, Union, Optional, Tuple, Any

import typer
from halo import Halo

from .project import choose_project
from . import db, utils
from .models import (
    SiteKey,
    SiteKeyValidator,
    CraftDetail,
    DetailDataType,
    CraftDetailValidator,
    craft_type_path_strings,
    CraftTypes,
)

app = typer.Typer(help="Manage Stilt Site Keys")
state = {"site_key": ""}


@app.command("audit")
def audit_sitekey(site_key: str = typer.Option(..., prompt=True)):
    """Audit a single site key for data errors"""
    spinner = Halo(text_color="blue")
    choose_project()
    styled_site_key = typer.style(site_key, fg=typer.colors.YELLOW, bold=True)
    try:
        spinner.start(f"Fetching {site_key}...")
        data = db.get_site_key(site_key)
        spinner.succeed()

        spinner.start(f"Validating data...")
        check_sitekey(**data)
        spinner.succeed()
        status = typer.style("passed", fg=typer.colors.GREEN, bold=True)
        typer.echo(f"{styled_site_key}: {status}")

    except (ValueError, TypeError) as err:
        spinner.fail("Error!")
        status = typer.style("failed", fg=typer.colors.RED, bold=True)
        typer.echo(f"{styled_site_key}: {status}")
        typer.echo(f"{err}")


@app.command("audit-all")
def audit_all_sitekeys():
    """Audit all project site keys for data errors"""
    spinner = Halo(text_color="blue")
    choose_project()
    spinner.start("Fetching data...")
    data = db.query_all_site_keys()
    spinner.succeed()

    for item in data:
        site_key = item[0]
        styled_site_key = typer.style(site_key, fg=typer.colors.YELLOW, bold=True)
        site_data = item[1]
        try:
            spinner.start(f"Validating {site_key}...")
            check_sitekey(**site_data)
            status = typer.style("passed", fg=typer.colors.GREEN, bold=True)
            spinner.succeed()
            typer.echo(f"{styled_site_key}: {status}")
        except (ValueError, TypeError) as err:
            spinner.fail()
            status = typer.style("failed", fg=typer.colors.RED, bold=True)
            typer.echo(f"{styled_site_key}: {status}")
            typer.echo(f"{err}")


@app.command("create")
def create_site_key():
    """Not yet implemented"""
    pass


@app.command()
def add_craft_detail(
    site_key: str = typer.Option(..., prompt=True),
    yes: bool = typer.Option(
        False, "--yes", "-y", help="Automatically confirm writes."
    ),
    skip_project: bool = typer.Option(
        False, "--skip-project", "-s", help="Use previous project if available."
    ),
    craft_type: CraftTypes = typer.Option(..., prompt=True, case_sensitive=False),
    detail_name: str = typer.Option(
        ...,
        prompt="Enter the detail path name (e.g. legFootAdded)",
        help="Variable name of the detail",
    ),
    data_type: DetailDataType = typer.Option(..., prompt=True, case_sensitive=False),
    title: str = typer.Option(..., prompt=True),
    default_value=typer.Option(
        "",
        prompt=True,
        help="A number, string, bool, or None (in the case of timestamps)",
    ),
    required: bool = typer.Option(..., prompt=True),
    editable: bool = typer.Option(..., prompt=True),
    min_value: Optional[int] = None,
    max_value: Optional[int] = None,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None,
) -> None:
    """Add a new or overwrite a dynamic craft detail."""
    try:
        # Parse the supplied inputs and prompt for any necessary extras.
        craft_detail = parse_add_craft_detail(
            craft_type=craft_type,
            detail_name=detail_name,
            data_type=data_type,
            title=title,
            default_value=default_value,
            required=required,
            editable=editable,
            min_value=min_value,
            max_value=max_value,
            min_length=min_length,
            max_length=max_length,
        )

        # Confirm the Firebase project in use.
        choose_project(skip=skip_project)
        # Check to make sure the site key exists.
        utils.check_site_key_exist(site_key)

        # Validate
        CraftDetailValidator(**asdict(craft_detail))
        craft_tuple = assemble_craft_detail(craft_type, detail_name, craft_detail)
        updates = build_craft_detail_updates([craft_tuple])

        msg_start = typer.style(
            "You are about to write this data for ", fg=typer.colors.YELLOW
        )
        msg_skey = typer.style(site_key, fg="green", bold=True)
        typer.echo(msg_start + msg_skey + ":")
        pprint(updates)
        confirm_text = typer.style(
            "Are you sure?", fg=typer.colors.BRIGHT_YELLOW, bold=True
        )

        # Handle auto confirm flag.
        if yes:
            is_confirmed = True
        else:
            is_confirmed = typer.confirm(confirm_text)

        if is_confirmed:
            spinner = Halo(text_color="blue")
            spinner.start(f"Updating {site_key}...")
            try:
                db.update_site_key(site_key=site_key, updates=updates)
                spinner.succeed()
                typer.secho("Update successful!", fg=typer.colors.GREEN, bold=True)
            except Exception as err:
                spinner.fail()
                raise err
        else:
            typer.echo("Exiting. No writes made.")

    except (ValueError, db.NotFound) as err:
        typer.secho(f"{err}", fg="red")
        typer.Abort()


def parse_add_craft_detail(
    craft_type: CraftTypes,
    detail_name: str,
    data_type: DetailDataType,
    title: str,
    default_value: Union[str, bool, int, float, datetime],
    required: bool,
    editable: bool,
    min_value: Union[int, float, None] = None,
    max_value: Union[int, float, None] = None,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None,
) -> CraftDetail:
    """Call user prompts if necessary data was left out."""
    if data_type == DetailDataType.boolean:
        # Convert the string value from the command line to a boolean.
        default_value = utils.convert_string_to_bool(default_value)
        craft_detail = validate_craft_detail(
            data_type=data_type,
            title=title,
            default_value=default_value,
            required=required,
            editable=editable,
        )
        return craft_detail
    elif data_type == DetailDataType.number:
        # Convert string from CLI to float.
        default_value = float(default_value)
        if min_value is None:
            min_value = utils.prompt("Please enter the min value", data_type=float)
        if max_value is None:
            max_value = utils.prompt("Please enter the max value", data_type=float)
        craft_detail = validate_craft_detail(
            data_type=data_type,
            title=title,
            default_value=default_value,
            required=required,
            editable=editable,
            min_value=min_value,
            max_value=max_value,
        )
        return craft_detail
    elif data_type == DetailDataType.string:

        if min_length is None:
            min_length = utils.prompt("Please enter the min length", data_type=int)
        if max_length is None:
            max_length = utils.prompt("Please enter the max length", data_type=int)
        craft_detail = validate_craft_detail(
            data_type=data_type,
            title=title,
            default_value=default_value,
            required=required,
            editable=editable,
            min_length=min_length,
            max_length=max_length,
        )
        return craft_detail
    elif data_type == DetailDataType.timestamp:
        # noinspection PyNoneFunctionAssignment
        default_value = utils.convert_string_to_none(default_value)
        craft_detail = validate_craft_detail(
            data_type=data_type,
            title=title,
            default_value=default_value,
            required=required,
            editable=editable,
            min_length=min_length,
            max_length=max_length,
        )
        return craft_detail
    else:
        raise ValueError(f"Unexpected data type for {data_type}")


def check_sitekey(
    name: str,
    timezone: str,
    managingCompanyID: str,
    validCraftTypes: List[int],
    validTaskTypes: List[int],
    validTaskStatusCodes: List[int],
    validEventTypes: List[int],
    customizations: dict,
) -> SiteKey:
    site_key: SiteKey = SiteKey(**locals())
    # Validate
    SiteKeyValidator(**asdict(site_key))

    return site_key


def validate_craft_detail(
    data_type: DetailDataType,
    title: str,
    default_value: Union[str, bool, int, float, datetime, None],
    required: bool,
    editable: bool,
    min_value: Union[int, float, None] = None,
    max_value: Union[int, float, None] = None,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None,
) -> CraftDetail:
    """
    Build and validate craft detail data.

    Return a tuple of craft type, detail name, and craft detail data.
    """
    craft_detail: CraftDetail = CraftDetail(**locals())
    # Validate
    CraftDetailValidator(**asdict(craft_detail))

    return craft_detail


def assemble_craft_detail(
    craft_type: CraftTypes, detail_name: str, craft_detail: CraftDetail
) -> Tuple[CraftTypes, str, CraftDetail]:
    """
    Check if craft type and detail name are correct data types and return a
    craft tuple
    """
    if isinstance(craft_type, CraftTypes) is False:
        raise ValueError("Expect craft_type to be in CraftTypes enum.")
    if isinstance(detail_name, str) is False:
        raise ValueError("Expected detail_name to be a string.")

    return craft_type, detail_name, craft_detail


def build_craft_detail_updates(
    data_list: List[Tuple[CraftTypes, str, CraftDetail]]
) -> dict:
    """
    Parse a list of craft detail tuples and return a single dictionary formatted
    for Firestore.
    """
    updates = dict()
    for item in data_list:
        craft_type, detail_name, detail_data = item
        craft_type_path = craft_type_path_strings[craft_type]
        updates[
            f"customizations.craftDetails.{craft_type_path}.{detail_name}"
        ] = detail_data.to_firestore()
    return updates


def main():
    app()


if __name__ == "__main__":
    main()
