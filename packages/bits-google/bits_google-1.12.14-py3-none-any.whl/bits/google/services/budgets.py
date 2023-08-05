# -*- coding: utf-8 -*-
"""Google Cloud Billing Budgets API."""

from bits.google.services.base import Base
# from googleapiclient.discovery import build
from google.auth.transport.requests import AuthorizedSession
# from google.cloud.billing.budgets_v1alpha1 import BudgetService
# from google.cloud.billing.budgets_v1alpha1.types.budget_service import ListBudgetsRequest


class CloudBillingBudgets(Base):
    """CloudBilling class."""

    def __init__(self, credentials):
        """Initialize a class instance."""
        # self.budgets = build('billingbudgets', 'v1', credentials=credentials)
        self.api_version = 'v1alpha1'
        self.base_url = 'https://billingbudgets.googleapis.com/%s' % (
            self.api_version,
        )
        self.credentials = credentials
        self.requests = AuthorizedSession(self.credentials)

        # self.client = BudgetService()

    def create_budget(self, billingAccountName, body):
        """Create a budget in the given billing account."""
        # params = {
        #     'billingAccountName': billingAccountName,
        #     'body': budgetName,
        # }
        # return self.budgets.budgets().create(**params).execute()
        url = '%s/billingAccounts/%s/budgets' % (
            self.base_url,
            billingAccountName,
        )
        return self.requests.post(url, json=body).json()

    def delete_budget(self, billingAccountName, budgetName):
        """Delete a budget."""
        # params = {
        #     'billingAccountName': billingAccountName,
        #     'budgetName': budgetName,
        # }
        # return self.budgets.budgets().delete(**params).execute()
        url = '%s/billingAccounts/%s/budgets/%s' % (
            self.base_url,
            billingAccountName,
            budgetName,
        )
        return self.requests.delete(url).json()

    def get_budget(self, billingAccountName, budgetName):
        """Return a budget for a given billing account."""
        # params = {
        #     'billingAccountName': billingAccountName,
        #     'budgetName': budgetName,
        # }
        # return self.budgets.budgets().get(**params).execute()
        url = '%s/billingAccounts/%s/budgets/%s' % (
            self.base_url,
            billingAccountName,
            budgetName,
        )
        return self.requests.get(url).json()

    def get_budgets(self, billingAccountName):
        """Return a list of budgets for the given billing account."""
        # params = {
        #     'billingAccountName': billingAccountName,
        # }
        # budgets = self.budgets.budgets()
        # request = budgets.list(**params)
        # return self.get_list_items(budgets, request, 'budgets')
        url = '%s/billingAccounts/%s/budgets' % (
            self.base_url,
            billingAccountName,
        )
        return self.requests.get(url).json().get('budgets', [])

    # def list_budgets(self, billingAccountName):
    #     """List budgets for a billing account."""
    #     list_budgets_request = ListBudgetsRequest(
    #         parent="billingAccounts/{}".format(billingAccountName)
    #     )
    #     budgets = []
    #     for budget in self.client.list_budgets(request=list_budgets_request):
    #         budgets.append(budget)
    #     return budgets

    def update_budget(self, billingAccountName, budgetName, body):
        """Update a budget in the given billing account."""
        # params = {
        #     'billingAccountName': billingAccountName,
        #     'body': budgetName,
        # }
        # return self.budgets.budgets().update(**params).execute()
        url = '%s/billingAccounts/%s/budgets/%s' % (
            self.base_url,
            billingAccountName,
            budgetName,
        )
        # example = {
        #     'budget': {
        #         'displayName': 'My Fancy Budget',
        #         'budgetFilter': {
        #             'projects': [
        #                 'projects/project_id_to_monitor',
        #             ]
        #         },
        #         'amount': {
        #             'specifiedAmount': {
        #                 'units': 500,
        #             }
        #         },
        #         'thresholdRules': {
        #             'thresholdPercent': 1.0,
        #         }
        #     }
        # }
        return self.requests.patch(url, json=body).json()
