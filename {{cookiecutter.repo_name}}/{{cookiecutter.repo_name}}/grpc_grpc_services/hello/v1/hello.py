
from person.services.company import ICompanyService
from person.utils import is_valid_uuid
from person.grpc_services.company.v1 import company_pb2, company_pb2_grpc
from person.grpc.decorators import config_grpc_service
import transaction
from person.models.company import Company

class CompaniesServicer(company_pb2_grpc.CompaniesServicer):

    def GetCompany(self, request, context):
        
        company_service = context.pyramid_request.find_service(ICompanyService)
        company = company_service.one(tax_id=request.taxId)

        company = company_pb2.Company(taxId=company.tax_id, name=company.name, uuid=str(company.uuid))
        return company_pb2.CompanyResponse(company=company)


@config_grpc_service
def configure(server, pyramid_app):
    company_pb2_grpc.add_CompaniesServicer_to_server(CompaniesServicer(), server)
