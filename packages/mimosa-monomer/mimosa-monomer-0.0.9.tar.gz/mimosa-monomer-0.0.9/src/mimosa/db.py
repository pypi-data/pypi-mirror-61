from typing import Tuple, List

from firebase_admin import firestore

from mimosa.models import SiteKeyUser, FirebaseDocClass

DocumentSnapshot = firestore.firestore.DocumentSnapshot


class NotFound(Exception):
    pass


class AlreadyExists(Exception):
    pass


def convert_doc_to_class(
    doc: DocumentSnapshot, DocClass: FirebaseDocClass
) -> FirebaseDocClass:
    """Convert a Firebase document to any class with the from_firestore_doc interface"""
    return DocClass.from_firestore_doc(doc)


def does_site_key_exist(site_key: str) -> bool:
    """Return whether the site key exists in Firestore"""
    db = firestore.client()
    doc = db.document(f"siteKeys/{site_key}").get()
    return doc.exists


def does_doc_exist(docPath: str) -> bool:
    """Return whether a document exist in Firestore"""
    db = firestore.client()
    doc = db.document(docPath).get()
    return doc.exists


def get_site_key(site_key: str) -> dict:
    """Download a site key document and return the data as a dictionary"""
    if site_key == "":
        raise ValueError("Site key was an empty string.")

    db = firestore.client()
    doc = db.document(f"siteKeys/{site_key}").get()
    if doc.exists is False:
        raise NotFound(f"Site key {site_key} does not exist")
    return doc.to_dict()


def get_sk_user(site_key: str, uid: str) -> dict:
    """Download and return a site key user document"""
    if site_key == "":
        raise ValueError("Site key was an empty string.")
    if uid == "":
        raise ValueError("UID was an empty string.")
    db = firestore.client()
    doc = db.document(f"siteKeys/{site_key}/siteKeyUsers/{uid}").get()
    if doc.exists is False:
        raise NotFound(f"Site key user {uid} was not found.")
    return doc.to_dict()


def query_all_site_keys() -> List[Tuple[str, dict]]:
    """Download all site key documents and return a list of tuples with (id, data)"""
    db = firestore.client()
    docs = db.collection("siteKeys").get()
    return [(doc.id, doc.to_dict()) for doc in docs]


def update_site_key(site_key: str, updates: dict) -> None:
    """Update a single site key document"""

    db = firestore.client()
    db.document(f"siteKeys/{site_key}").update(updates)
    return


def set_site_key(site_key: str, updates: dict) -> None:
    """Set a single site key document"""

    db = firestore.client()
    db.document(f"siteKeys/{site_key}").set(updates)
    return


def set_site_key_company(site_key: str, site_key_company: str, updates: dict) -> None:
    """Set a single site key company document"""

    db = firestore.client()
    db.document(f"siteKeys/{site_key}/siteKeyCompanies/{site_key_company}").set(updates)
    return
