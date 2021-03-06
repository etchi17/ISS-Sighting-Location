from app import *
import pytest

read_data_from_file_into_dict()
input = "input"

def test_help():
    assert isinstance(help(),str) == True

def test_read_data_help():
    assert isinstance(read_data_help(),str) == True

def test_read_data_from_file_into_dict():
    assert isinstance(read_data_from_file_into_dict(),str) == True

def test_get_all_epochs():
    assert isinstance(get_all_epochs(),str) == True    

def test_get_epoch_data():
    assert isinstance(get_epoch_data(input),dict) == True

def test_get_all_countries():
    assert isinstance(get_all_countries(),dict) == True

def test_get_country_data():
    assert isinstance(get_country_data(input),str) == True

def test_get_all_regions():
    assert isinstance(get_all_regions(input),dict) == True

def test_get_region_data():
    assert isinstance(get_region_data(input,input),str) == True

def test_get_all_cities():
    assert isinstance(get_all_cities(input,input),dict) == True

def test_get_city_data():
    assert isinstance(get_city_data(input,input,input),str) == True
