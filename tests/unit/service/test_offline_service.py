import pytest
import pandas as pd
from unittest.mock import patch
from app.services.offline_service import OfflineService

@pytest.mark.asyncio
async def test_get_csv_file_not_found_returns_message(capsys):
    with patch("pandas.read_csv", side_effect=FileNotFoundError), \
         patch("os.path.dirname", side_effect=lambda x=None: "/root" if x is None else "/root"), \
         patch("os.path.abspath", return_value="/root/file.py"):
        result = await OfflineService.get_csv(2021, "expo", "vinhos")
        assert result == "Arquivo não encontrado"
        captured = capsys.readouterr()
        assert "não foi encontrado" in captured.out

@pytest.mark.asyncio
async def test_get_csv_empty_data_error_returns_message(capsys):
    with patch("pandas.read_csv", side_effect=pd.errors.EmptyDataError), \
         patch("os.path.dirname", side_effect=lambda x=None: "/root" if x is None else "/root"), \
         patch("os.path.abspath", return_value="/root/file.py"):
        result = await OfflineService.get_csv(2020, "expo", "vinhos")
        assert result == "Arquivo vazio ou sem dados"
        captured = capsys.readouterr()
        assert "está vazio ou não possui cabeçalho/dados" in captured.out

@pytest.mark.asyncio
async def test_get_csv_generic_exception_returns_message(capsys):
    with patch("pandas.read_csv", side_effect=Exception("fail")), \
         patch("os.path.dirname", side_effect=lambda x=None: "/root" if x is None else "/root"), \
         patch("os.path.abspath", return_value="/root/file.py"):
        result = await OfflineService.get_csv(2019, "expo", "vinhos")
        assert result == "Ocorreu um erro inesperado ao ler o arquivo"
        captured = capsys.readouterr()
        assert "Ocorreu um erro inesperado ao ler o arquivo" in captured.out

@pytest.mark.asyncio
async def test_get_csv_subdir_none_path():
    mock_df = pd.DataFrame([{"a": 1}])
    with patch("pandas.read_csv", return_value=mock_df) as mock_read_csv, \
         patch("os.path.dirname", side_effect=lambda x=None: "/root" if x is None else "/root"), \
         patch("os.path.abspath", return_value="/root/file.py"):
        result = await OfflineService.get_csv(2023, "expo", None)
        assert result is not None
        args, kwargs = mock_read_csv.call_args
        assert "data\\expo\\" in args[0] or "data/expo/" in args[0]

@pytest.mark.asyncio
async def test_get_csv_empty_subdir():
    mock_df = pd.DataFrame([{"a": 1}])
    with patch("pandas.read_csv", return_value=mock_df) as mock_read_csv, \
         patch("os.path.dirname", side_effect=lambda x=None: "/root" if x is None else "/root"), \
         patch("os.path.abspath", return_value="/root/file.py"):
        result = await OfflineService.get_csv(2024, "expo", "")
        assert result is not None
        args, kwargs = mock_read_csv.call_args
        assert "data\\expo\\" in args[0] or "data/expo/" in args[0]

@pytest.mark.asyncio
async def test_get_csv_path_construction_with_special_chars():
    mock_df = pd.DataFrame([{"a": 1}])
    with patch("pandas.read_csv", return_value=mock_df) as mock_read_csv, \
         patch("os.path.dirname", side_effect=lambda x=None: "/root" if x is None else "/root"), \
         patch("os.path.abspath", return_value="/root/file.py"):
        result = await OfflineService.get_csv(2025, "expô", "vinhõs")
        assert result is not None
        args, kwargs = mock_read_csv.call_args
        assert "data\\expô\\vinhõs" in args[0] or "data/expô/vinhõs" in args[0]
        @pytest.mark.asyncio
        async def test_get_csv_success_returns_json():
            mock_df = pd.DataFrame([{"a": 1, "b": 2}, {"a": 3, "b": 4}])
            expected_json = mock_df.to_json(orient='records', indent=1, force_ascii=False)
            with patch("pandas.read_csv", return_value=mock_df) as mock_read_csv, \
                 patch("os.path.dirname", side_effect=lambda x=None: "/root" if x is None else "/root"), \
                 patch("os.path.abspath", return_value="/root/file.py"):
                result = await OfflineService.get_csv(2022, "expo", "uvas")
                assert result == expected_json
                mock_read_csv.assert_called_once()
                args, kwargs = mock_read_csv.call_args
                assert "data\\expo\\uvas" in args[0] or "data/expo/uvas" in args[0]
                assert "2022.csv" in args[0]

        @pytest.mark.asyncio
        async def test_get_csv_file_not_found_returns_message(capsys):
            with patch("pandas.read_csv", side_effect=FileNotFoundError), \
                 patch("os.path.dirname", side_effect=lambda x=None: "/root" if x is None else "/root"), \
                 patch("os.path.abspath", return_value="/root/file.py"):
                result = await OfflineService.get_csv(2021, "expo", "vinhos")
                assert result == "Arquivo não encontrado"
                captured = capsys.readouterr()
                assert "não foi encontrado" in captured.out

        @pytest.mark.asyncio
        async def test_get_csv_empty_data_error_returns_message(capsys):
            with patch("pandas.read_csv", side_effect=pd.errors.EmptyDataError), \
                 patch("os.path.dirname", side_effect=lambda x=None: "/root" if x is None else "/root"), \
                 patch("os.path.abspath", return_value="/root/file.py"):
                result = await OfflineService.get_csv(2020, "expo", "vinhos")
                assert result == "Arquivo vazio ou sem dados"
                captured = capsys.readouterr()
                assert "está vazio ou não possui cabeçalho/dados" in captured.out

        @pytest.mark.asyncio
        async def test_get_csv_generic_exception_returns_message(capsys):
            with patch("pandas.read_csv", side_effect=Exception("fail")), \
                 patch("os.path.dirname", side_effect=lambda x=None: "/root" if x is None else "/root"), \
                 patch("os.path.abspath", return_value="/root/file.py"):
                result = await OfflineService.get_csv(2019, "expo", "vinhos")
                assert result == "Ocorreu um erro inesperado ao ler o arquivo"
                captured = capsys.readouterr()
                assert "Ocorreu um erro inesperado ao ler o arquivo" in captured.out

        @pytest.mark.asyncio
        async def test_get_csv_subdir_none_path():
            mock_df = pd.DataFrame([{"a": 1}])
            with patch("pandas.read_csv", return_value=mock_df) as mock_read_csv, \
                 patch("os.path.dirname", side_effect=lambda x=None: "/root" if x is None else "/root"), \
                 patch("os.path.abspath", return_value="/root/file.py"):
                result = await OfflineService.get_csv(2023, "expo", None)
                assert result is not None
                args, kwargs = mock_read_csv.call_args
                assert "data\\expo\\" in args[0] or "data/expo/" in args[0]

        @pytest.mark.asyncio
        async def test_get_csv_empty_subdir():
            mock_df = pd.DataFrame([{"a": 1}])
            with patch("pandas.read_csv", return_value=mock_df) as mock_read_csv, \
                 patch("os.path.dirname", side_effect=lambda x=None: "/root" if x is None else "/root"), \
                 patch("os.path.abspath", return_value="/root/file.py"):
                result = await OfflineService.get_csv(2024, "expo", "")
                assert result is not None
                args, kwargs = mock_read_csv.call_args
                assert "data\\expo\\" in args[0] or "data/expo/" in args[0]

        @pytest.mark.asyncio
        async def test_get_csv_path_construction_with_special_chars():
            mock_df = pd.DataFrame([{"a": 1}])
            with patch("pandas.read_csv", return_value=mock_df) as mock_read_csv, \
                 patch("os.path.dirname", side_effect=lambda x=None: "/root" if x is None else "/root"), \
                 patch("os.path.abspath", return_value="/root/file.py"):
                result = await OfflineService.get_csv(2025, "expô", "vinhõs")
                assert result is not None
                args, kwargs = mock_read_csv.call_args
                assert "data\\expô\\vinhõs" in args[0] or "data/expô/vinhõs" in args[0]
