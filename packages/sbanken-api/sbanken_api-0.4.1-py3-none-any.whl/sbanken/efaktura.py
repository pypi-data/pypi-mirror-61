from .auth import Auth
from .const import BANK_SCOPE


class Efaktura:
    """ Class that represents an eFaktura in Sbanken """

    def __init__(self, raw_data: dict, auth: Auth):
        if "item" in raw_data:
            self.raw_data = raw_data["item"]
        else:
            self.raw_data = raw_data
        self.auth = auth

    @property
    def efaktura_id(self) -> str:
        return self.raw_data["eFakturaId"]

    @property
    def issuer_id(self) -> str:
        return self.raw_data["issuerId"]

    @property
    def issuer_name(self) -> str:
        return self.raw_data["issuerName"]

    @property
    def reference(self) -> str:
        return self.raw_data["eFakturaReference"]

    @property
    def document_type(self) -> str:
        return self.raw_data["documentType"]

    @property
    def status(self) -> str:
        return self.raw_data["status"]

    @property
    def kid(self) -> str:
        return self.raw_data["kid"]

    @property
    def original_due_date(self) -> str:
        return self.raw_data["originalDueDate"]

    @property
    def original_amount(self) -> float:
        return self.raw_data["originalAmount"]

    @property
    def minimum_amount(self) -> float:
        return self.raw_data["minimumAmount"]

    @property
    def updated_due_date(self) -> str:
        return self.raw_data["updatedDueDate"]

    @property
    def updated_amount(self) -> float:
        return self.raw_data["updatedAmount"]
