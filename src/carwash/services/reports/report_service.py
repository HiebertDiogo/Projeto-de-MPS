from services.reports.html_report import HTMLReport
from services.reports.report_decorator import LoggingReportDecorator
from carwash.logger.python_logging_adapter import build_python_logging_adapter

class ReportService:
    def execute_html_report(self):
        logger = build_python_logging_adapter("report")
        report = HTMLReport()
        report = LoggingReportDecorator(report, logger)

        return report.generate()
    
