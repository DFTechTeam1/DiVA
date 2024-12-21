import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from sqlalchemy.ext.asyncio import AsyncSession
from utils.custom_errors import DatabaseQueryError, DataNotFoundError


@pytest.mark.asyncio
async def test_retrieve_all_with_available_data(example_table):
    mock_session = AsyncMock(spec=AsyncSession)
    mock_result = MagicMock()
    mock_result.__tablename__ = "filled_table"
    mock_result.fetchall.return_value = [
        MagicMock(_mapping={"id": 1, "name": "Item 1"}),
        MagicMock(_mapping={"id": 2, "name": "Item 2"}),
    ]

    mock_session.execute.return_value = mock_result

    with patch("services.postgres.connection.database_connection") as mock_db_conn:
        mock_db_conn.return_value.connect.return_value.__aenter__.return_value = (
            mock_session
        )
        from utils.query.general import retrieve_all

        result = await retrieve_all(table_model=example_table)

        assert len(result) == 2
        assert result[0]["name"] == "Item 1"
        assert result[1]["name"] == "Item 2"

        mock_session.execute.assert_called_once()
        mock_session.close.assert_called_once()


@pytest.mark.asyncio
async def test_retrieve_all_with_no_data(example_table):
    mock_session = AsyncMock(spec=AsyncSession)
    mock_result = MagicMock()
    mock_result.__tablename__ = "empty_table"
    mock_result.fetchall.return_value = []

    mock_session.execute.return_value = mock_result

    with patch("utils.query.general.database_connection") as mock_db_conn:
        mock_db_conn.return_value.connect.return_value.__aenter__.return_value = (
            mock_session
        )
        from utils.query.general import retrieve_all

        with pytest.raises(DataNotFoundError):
            await retrieve_all(table_model=example_table)

        mock_session.execute.assert_called_once()
        mock_session.close.assert_called_once()


@pytest.mark.asyncio
async def test_retrieve_all_with_query_error(example_table):
    mock_session = AsyncMock(spec=AsyncSession)
    mock_result = MagicMock()
    mock_result.__tablename__ = "error_table"
    mock_session.execute.side_effect = Exception("Invalid database query.")

    with patch("utils.query.general.database_connection") as mock_db_conn:
        mock_db_conn.return_value.connect.return_value.__aenter__.return_value = (
            mock_session
        )
        from utils.query.general import retrieve_all

        with pytest.raises(DatabaseQueryError):
            await retrieve_all(table_model=example_table)

        mock_session.rollback.assert_called_once()
        mock_session.close.assert_called_once()


@pytest.mark.asyncio
async def test_retrieve_all_with_invalid_table(example_table):
    mock_session = AsyncMock(spec=AsyncSession)
    mock_session.execute.side_effect = Exception("Invalid database query.")

    with patch("utils.query.general.database_connection") as mock_db_conn:
        mock_db_conn.return_value.connect.return_value.__aenter__.return_value = (
            mock_session
        )
        from utils.query.general import retrieve_all

        with pytest.raises(DatabaseQueryError):
            await retrieve_all(table_model=example_table)

        mock_session.rollback.assert_called_once()
        mock_session.close.assert_called_once()
