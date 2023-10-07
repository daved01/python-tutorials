import csv
import pytest
import tempfile

from my_code import FirstClass, SecondClass, ThirdClass


class TestExampleBasic:
    # Basic test
    def test_double_pos_val_pass(self):
        first_class = FirstClass()
        res = first_class.double_pos_int(2)
        assert res == 4

    @pytest.mark.parametrize("val_in, val_should", [(1, 2), (3, 6), (10, 20)])
    def test_double_pos_val_pass(self, val_in, val_should):
        first_class = FirstClass()
        res = first_class.double_pos_int(val_in)
        assert res == val_should

    def test_double_pos_val_fail(self):
        first_class = FirstClass()
        with pytest.raises(RuntimeError):
            _ = first_class.double_pos_int(-1)


class TestExampleFixtures:
    # Fixtures
    @pytest.fixture
    def setup_first_class(self):
        return FirstClass()

    def test_double_pos_val_fixture_pass(self, setup_first_class):
        res = setup_first_class.double_pos_int(2)
        assert res == 4

    # Parametrization with fixtures
    @pytest.fixture
    def input_data(self):
        return {"val1": 1, "val2": 2, "val3": 3}

    @pytest.mark.parametrize("input, expected", [("input_data", [1, 2, 3])])
    def test_unpack_dict(self, setup_first_class, request, input, expected):
        input_dict = request.getfixturevalue(input)
        res = setup_first_class.unpack_dict(input_dict)
        assert res == expected


class TestExamplePatchingMocking:
    def test_add_to_remote_number(self, mocker):
        second_class = SecondClass("https://url.com/fake")
        mocker.patch("my_code.SecondClass._get_request", return_value={"three": 3})
        res = second_class.add_to_remote_number(5, "three")
        assert res == 8

    def test_get_request_mocker(self, mocker):
        second_class = SecondClass("https://url.com/fake")

        class MockGet:
            def __init__(self):
                pass

            def raise_for_status(self):
                pass

            def json(self):
                return {"a": 1}

        mocker.patch("requests.get", return_value=MockGet())
        res = second_class._get_request("fake")
        assert res == {"a": 1}

    def test_add_to_remote_number_monkeypatch(self, monkeypatch):
        second_class = SecondClass("https://url.com/fake")

        def mock_request(*args):
            return {"three": 3}

        monkeypatch.setattr(SecondClass, "_get_request", mock_request)

        res = second_class.add_to_remote_number(5, "three")
        assert res == 8


class TestThirdClass:
    def test_write_to_csv(self):
        third_class = ThirdClass()
        data = [["A", "2"], ["B", "3"]]

        with tempfile.TemporaryDirectory() as temp_dir:
            filename = temp_dir + "my_file.csv"
            third_class.write_to_csv(filename, data)

            # Read file content
            with open(filename, "r", encoding="utf-8") as filehandler:
                reader = csv.reader(filehandler)
                saved_data = []
                for row in reader:
                    saved_data.append(row)

            assert saved_data == data
