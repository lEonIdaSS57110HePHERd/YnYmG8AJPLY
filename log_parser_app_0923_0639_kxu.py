# 代码生成时间: 2025-09-23 06:39:07
import re
import logging
from django.http import JsonResponse
from django.views import View
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

# 配置日志记录器
logger = logging.getLogger(__name__)

class LogParser:
    """
    日志文件解析工具。
    """
    def __init__(self):
        self.log_file_path = getattr(settings, 'LOG_FILE_PATH', None)
        if not self.log_file_path:
            raise ImproperlyConfigured('LOG_FILE_PATH must be set in settings')

    def parse_log_file(self):
        """
        解析日志文件内容，并返回关键信息。
        """
        try:
            with open(self.log_file_path, 'r') as file:
                logs = file.readlines()
                parsed_logs = self._extract_critical_information(logs)
                return parsed_logs
        except FileNotFoundError:
            logger.error(f'Log file not found at {self.log_file_path}')
            raise
        except Exception as e:
            logger.error(f'Error occurred while parsing log file: {e}')
            raise

    def _extract_critical_information(self, logs):
        """
        从日志中提取关键信息。
        """
        # 正则表达式用于匹配日志中的日期、级别和消息
        log_pattern = re.compile(r'(\d{4}-\d{2}-\d{2}) (\w+) (.*)')
        critical_info = []
        for log in logs:
            match = log_pattern.match(log.strip())
            if match:
                date, level, message = match.groups()
                critical_info.append({'date': date, 'level': level, 'message': message})
        return critical_info


class LogParseView(View):
    """
    日志文件解析视图。
    """
    def get(self, request):
        """
        返回解析日志文件的内容。
        """
        try:
            log_parser = LogParser()
            parsed_logs = log_parser.parse_log_file()
            return JsonResponse(parsed_logs, safe=False)
        except Exception as e:
            logger.error(f'Error occurred while parsing log file: {e}')
            return JsonResponse({'error': 'Failed to parse log file'}, status=500)

# URL配置
log_parser_urls = [
    {
        'path': 'parse-log/',
        'view': LogParseView.as_view(),
        'name': 'parse-log'
    }
]
