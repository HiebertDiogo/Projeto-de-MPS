from reports.abstract_report import AbstractReport

class ReportDecorator(AbstractReport):
    def __init__(self, report: AbstractReport):
        self._report = report

    def generate(self):
        return self._report.generate()
    
class LoggingReportDecorator(ReportDecorator):
    def __init__(self, report: AbstractReport, logger):
        super().__init__(report)
        self.logger = logger

    def generate(self):
        self.logger.log_info("Iniciando geração do relatório", {})
        
        result = self._report.generate()
        
        self.logger.log_info("Relatório finalizado", {})
        
        return result