from dependency_injector import containers, providers

from ..services import FileHandlerService, FileReaderService


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    file_handler = providers.Factory(
        FileHandlerService,
        type='csv',
    )

    file_reader = providers.Factory(
        FileReaderService,
        file_handler=file_handler,
        duplicates=False
    )