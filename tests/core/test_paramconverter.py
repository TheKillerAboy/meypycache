from pytest import fixture
from meypycache.core import paramconverter
import pytest

@fixture
def no_inputs_func():
    def no_inputs():
        pass
    return no_inputs

def test_link_parameters_no_inputs(no_inputs_func):
    assert paramconverter.ParameterConverter.link_parameters(no_inputs_func,(),{}) == {}

@fixture
def args_only_inputs_func():
    def args_only_inputs(a,b):
        pass
    return args_only_inputs

def test_link_parameters_args_only_inputs(args_only_inputs_func):
    assert paramconverter.ParameterConverter.link_parameters(args_only_inputs_func,('a','b'),{}) == {
        'a':'a',
        'b':'b'
    }

@fixture
def kwargs_only_inputs_func():
    def kwargs_only_inputs(a = None,b = None):
        pass
    return kwargs_only_inputs

def test_link_parameters_kwargs_only_inputs(kwargs_only_inputs_func):
    assert paramconverter.ParameterConverter.link_parameters(kwargs_only_inputs_func,(),{'a':'a','b':'b'}) == {
        'a':'a',
        'b':'b'
    }

@fixture
def full_inputs_func():
    def full_inputs(a, b, c = None,d = None):
        pass
    return full_inputs

def test_link_parameters_full_inputs(full_inputs_func):
    assert paramconverter.ParameterConverter.link_parameters(full_inputs_func,('a','b'),{'c':'c','d':'d'}) == {
        'a':'a',
        'b':'b',
        'c':'c',
        'd':'d'
    }

@fixture
def converter():
    pc = paramconverter.ParameterConverter()
    return pc

def test_register(converter):
    @converter.register('repo')
    def repo_converter(repo):
        pass

    assert 'repo' in converter.converters
    assert converter.converters['repo'] == repo_converter

def test_invalid_register(converter):
    try:
        @converter.register('repo')
        def repo_converter():
            pass
        assert False
    except paramconverter.InvalidConveterMethod:
        assert True

@fixture
def converter_with_converstions(converter):
    @converter.register('a')
    def a(a):
        return ord(a)

    @converter.register('c')
    def c(c):
        return c*5

    return converter

@pytest.mark.parametrize(
    'arg,input,output',
    [
        ('a','k',107),
        ('b','hello','hello'),
        ('c','p','ppppp')
    ]
)
def test_convert_by_name(converter_with_converstions,arg,input,output):
    assert converter_with_converstions.convert_by_name(arg, input) == output
