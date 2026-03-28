from __future__ import annotations

import logging

from carwash.logger.i_logger import ILogger


class PythonLoggingAdapter(ILogger):
    """Adapter (GoF Adapter — Object Adapter via composição).

    Adaptee : logging.Logger  (stdlib Python)
    Target  : ILogger

    Incompatibilidades de interface resolvidas aqui:
      1. Nomes de método: log_info / log_warning / log_error
                       →  .info   / .warning   / .error
      2. Assinatura: log_info(message: str, context: dict)
                  →  .info(msg: str, *args, **kwargs)
         O parâmetro context: dict não existe na interface do Adaptee;
         o Adapter serializa o dicionário inline na mensagem formatada.
      3. Configuração do Formatter (formato, datefmt) é responsabilidade
         interna do Adapter — os clientes não precisam saber disso.
    """

    def __init__(self, logger: logging.Logger) -> None:
        self._logger = logger  # Adaptee armazenado por composição

    # ---- Implementação do Target (ILogger) ----

    def log_info(self, message: str, context: dict) -> None:
        # Traduz: context: dict → formatação inline aceita pelo Adaptee
        self._logger.info("%s | context=%s", message, context)

    def log_warning(self, message: str, context: dict) -> None:
        self._logger.warning("%s | context=%s", message, context)

    def log_error(self, message: str, context: dict) -> None:
        self._logger.error("%s | context=%s", message, context)


def build_python_logging_adapter(
    name: str,
    level: int = logging.DEBUG,
) -> PythonLoggingAdapter:
    """Factory: configura o Adaptee (logging.Logger) e retorna o Adapter pronto.

    O guard `if not logger.handlers` evita handlers duplicados caso a função
    seja chamada mais de uma vez com o mesmo nome (ex.: em testes).
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter(
                fmt="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        )
        logger.addHandler(handler)

    return PythonLoggingAdapter(logger)
