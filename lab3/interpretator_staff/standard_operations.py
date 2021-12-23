import copy
import sys
import numpy as np

from interpretator_staff.standard_converts import Var


class Operations:
    def binary_plus(self, _val1, _val2, standard_conversions):  # ADDITION or OR
        no_error = True
        res_type = 'UNDEF'
        if type(_val1) == list:
            _val1 = _val1[1]
            res = copy.deepcopy(_val1)
            if type(_val2) == list:
                _val2 = _val2[1]
                for i in range(min(len(_val1), len(_val2))):
                    res[i] = self.binary_plus(_val1[i], _val2[i], standard_conversions)
            else:
                for i in range(len(_val1)):
                    res[i] = self.binary_plus(_val1[i], _val2, standard_conversions)
            return res
        else:
            if (_val1.type == 'UNDEF') and not (_val2.type == 'UNDEF'):
                _val1.type = _val2.type
            if (_val2.type == 'UNDEF') and not (_val1.type == 'UNDEF'):
                _val2.type = _val1.type
            if (_val2.type == 'UNDEF') and (_val1.type == 'UNDEF'):
                return Var()
            x1 = _val1.value
            x2 = _val2.value
            if _val1.type == _val2.type:
                if _val1.type == "NUMERIC":
                    return Var('NUMERIC', x1 + x2)
                elif _val1.type == "LOGIC":
                    if (x1 is not None) and (x2 is not None):
                        return Var('LOGIC', bool(x1) or bool(x2))
                    else:
                        if x1 or x2:
                            return Var('LOGIC', True)
                        else:
                            return Var('LOGIC', None)

                elif _val1.type == "STRING":
                    no_error = False
                    sys.stderr.write(f'Illegal operation: type STRING\n')
            else:
                if _val1.left and _val2.right:
                    no_error = False
                    sys.stderr.write(f'Illegal operation: type conversion double definition is illegal\n')
                elif _val1.left:
                    res_type = _val1.type
                    _val1.left = False
                elif _val2.right:
                    res_type = _val2.type
                    _val2.right = False
                else:
                    no_error = False
                    sys.stderr.write(f'Невозможно посчитать, будьте добры указать, куда мне приводить тип\n')
                if no_error:
                    if res_type == "NUMERIC":
                        return Var('NUMERIC',
                                   standard_conversions.converting(_val1, 'NUMERIC').value + standard_conversions.converting(
                                       _val2, 'NUMERIC').value)
                    elif res_type == "LOGIC":
                        x1 = bool(standard_conversions.converting(_val1, 'LOGIC').value)
                        x2 = bool(standard_conversions.converting(_val2, 'LOGIC').value)
                        if (x1 is not None) and (x2 is not None):
                            return Var('LOGIC', bool(x1) or bool(x2))
                        else:
                            if x1 or x2:
                                return Var('LOGIC', True)
                            else:
                                return Var('LOGIC', None)
                    elif res_type == "STRING":
                        sys.stderr.write(f'Illegal operation: type STRING\n')

    def bin_minus(self, _val1, _val2, standard_conversions):  # SUBTRACTION or XOR
        no_error = True
        res_type = 'UNDEF'
        if type(_val1) == np.ndarray:
            res = copy.deepcopy(_val1)
            if type(_val2) == np.ndarray:
                for i in range(min(len(_val1), len(_val2))):
                    res[i] = self.bin_minus(_val1[i], _val2[i], standard_conversions)
            else:
                for i in range(len(_val1)):
                    res[i] = self.bin_minus(_val1[i], _val2, standard_conversions)
            return res
        else:
            if (_val1.type == 'UNDEF') and not (_val2.type == 'UNDEF'):
                _val1.type = _val2.type
            if (_val2.type == 'UNDEF') and not (_val1.type == 'UNDEF'):
                _val2.type = _val1.type
            if (_val2.type == 'UNDEF') and (_val1.type == 'UNDEF'):
                return Var()
            x1 = _val1.value
            x2 = _val2.value
            if _val1.type == _val2.type:
                if _val1.type == "NUMERIC":
                    return Var('NUMERIC', x1 - x2)
                elif _val1.type == "LOGIC":
                    if (x1 != None) and (x2 != None):
                        return Var('LOGIC', (bool(x1) and not bool(x2)) or (bool(x2) and not bool(x1)))
                    else:
                        return Var('LOGIC', None)
                elif _val1.type == "STRING":
                    no_error = False
                    sys.stderr.write(f'Illegal operation: type STRING\n')
            else:
                if _val1.left and _val2.right:
                    no_error = False
                    sys.stderr.write(f'Illegal operation: type conversion double definition is illegal\n')
                elif _val1.left:
                    res_type = _val1.type
                    _val1.left = False
                elif _val2.right:
                    res_type = _val2.type
                    _val2.right = False
                else:
                    no_error = False
                    sys.stderr.write(f'Невозможно посчитать, будьте добры указать, куда мне приводить тип\n')
                if no_error:
                    if res_type == "NUMERIC":
                        return Var('NUMERIC',
                                   standard_conversions.converting(_val1, 'NUMERIC').value + standard_conversions.converting(
                                       _val2,
                                       'NUMERIC').value)
                    elif res_type == "LOGIC":
                        x1 = bool(standard_conversions.converting(_val1, 'LOGIC').value)
                        x2 = bool(standard_conversions.converting(_val2, 'LOGIC').value)
                        if (x1 is not None) and (x2 is not None):
                            return Var('LOGIC', (bool(x1) and not bool(x2)) or (bool(x2) and not bool(x1)))
                        else:
                            return Var('LOGIC', None)
                    elif res_type == "STRING":
                        sys.stderr.write(f'Illegal operation: type STRING\n')

    def bin_multi(self, _val1, _val2, standard_conversions):  # MULTIPLICATION or AND
        no_error = True
        res_type = 'UNDEF'
        if type(_val1) == list:
            _val1 = _val1[1]
            res = copy.deepcopy(_val1)
            if type(_val2) == list:
                _val2 = _val2[1]
                for i in range(min(len(_val1), len(_val2))):
                    res[i] = self.bin_multi(_val1[i], _val2[i], standard_conversions)
            else:
                for i in range(len(_val1)):
                    res[i] = self.bin_multi(_val1[i], _val2, standard_conversions)
            return res
        else:
            if (_val1.type == 'UNDEF') and not (_val2.type == 'UNDEF'):
                _val1.type = _val2.type
            if (_val2.type == 'UNDEF') and not (_val1.type == 'UNDEF'):
                _val2.type = _val1.type
            if (_val2.type == 'UNDEF') and (_val1.type == 'UNDEF'):
                return Var()
            x1 = _val1.value
            x2 = _val2.value
            if _val1.type == _val2.type:
                if _val1.type == "NUMERIC":
                    return Var('NUMERIC', x1 * x2)
                elif _val1.type == "LOGIC":
                    if (x1 != None) and (x2 != None):
                        return Var('LOGIC', bool(x1) or bool(x2))
                    else:
                        if (not x1 or not x2) or (x1 == x2):
                            return Var('LOGIC', None)
                        else:
                            return Var('LOGIC', False)

                elif _val1.type == "STRING":
                    no_error = False
                    sys.stderr.write(f'Illegal operation: type STRING\n')
            else:
                if _val1.left and _val2.right:
                    no_error = False
                    sys.stderr.write(f'Illegal operation: type conversion double definition is illegal\n')
                elif _val1.left:
                    res_type = _val1.type
                    _val1.left = False
                elif _val2.right:
                    res_type = _val2.type
                    _val2.right = False
                else:
                    no_error = False
                    sys.stderr.write(f'Невозможно посчитать, будьте добры указать, куда мне приводить тип\n')
                if no_error:
                    if res_type == "NUMERIC":
                        return Var('NUMERIC',
                                   standard_conversions.converting(_val1, 'NUMERIC').value + standard_conversions.converting(
                                       _val2, 'NUMERIC').value)
                    elif res_type == "LOGIC":
                        x1 = bool(standard_conversions.converting(_val1, 'LOGIC').value)
                        x2 = bool(standard_conversions.converting(_val2, 'LOGIC').value)
                        if (x1 != None) and (x2 != None):
                            return Var('LOGIC', bool(x1) or bool(x2))
                        else:
                            if (not x1 or not x2) or (x1 == x2):
                                return Var('LOGIC', None)
                            else:
                                return Var('LOGIC', False)
                    elif res_type == "STRING":
                        sys.stderr.write(f'Illegal operation: type STRING\n')

    # binary slash -- DIVISION or NAND (Sheffer's stroke)
    def bin_slash(self, _val1, _val2, standard_conversions):
        no_error = True
        res_type = 'UNDEF'
        if type(_val1) == np.ndarray:
            res = copy.deepcopy(_val1)
            if type(_val2) == np.ndarray:
                for i in range(min(len(_val1), len(_val2))):
                    res[i] = self.bin_slash(_val1[i], _val2[i], standard_conversions)
            else:
                for i in range(len(_val1)):
                    res[i] = self.bin_slash(_val1[i], _val2, standard_conversions)
            return res
        else:
            if (_val1.type == 'UNDEF') and not (_val2.type == 'UNDEF'):
                _val1.type = _val2.type
            elif (_val2.type == 'UNDEF') and not (_val1.type == 'UNDEF'):
                _val2.type = _val1.type
            elif (_val2.type == 'UNDEF') and (_val1.type == 'UNDEF'):
                return Var()
            x1 = _val1.value
            x2 = _val2.value
            if _val1.type == _val2.type:
                if _val1.type == "NUMERIC":
                    return Var('NUMERIC', x1 // x2)
                elif _val1.type == "LOGIC":
                    if (x1 != None) and (x2 != None):  # bcoz False and None are too close
                        return Var('LOGIC', not (bool(x1) and bool(x2)))
                    else:
                        if (x1 or x2) or (x1 == x2):
                            return Var('LOGIC', None)
                        else:
                            return Var('LOGIC', True)

                elif _val1.type == "STRING":
                    no_error = False
                    sys.stderr.write(f'Illegal operation: type STRING\n')
            else:
                if _val1.left and _val2.right:
                    no_error = False
                    sys.stderr.write(f'Illegal operation: type conversion double definition is illegal\n')
                elif _val1.left:
                    res_type = _val1.type
                    _val1.left = False
                elif _val2.right:
                    res_type = _val2.type
                    _val2.right = False
                else:
                    no_error = False
                    sys.stderr.write(f'Невозможно посчитать, будьте добры указать, куда мне приводить тип\n')
                if no_error:
                    if res_type == "NUMERIC":
                        return Var('NUMERIC',
                                   standard_conversions.converting(_val1, 'NUMERIC').value + standard_conversions.converting(
                                       _val2, 'NUMERIC').value)
                    elif res_type == "LOGIC":
                        x1 = bool(standard_conversions.converting(_val1, 'LOGIC').value)
                        x2 = bool(standard_conversions.converting(_val2, 'LOGIC').value)
                        if (x1 is not None) and (x2 is not None):
                            return Var('LOGIC', not (bool(x1) or bool(x2)))
                        else:
                            if (x1 or x2) or (x1 == x2):
                                return Var('LOGIC', None)
                            else:
                                return Var('LOGIC', True)
                    elif res_type == "STRING":
                        sys.stderr.write(f'Illegal operation: type STRING\n')

    # binary caret -- EXPONENTIATION or NOR (Peirce's arrow)
    def bin_caret(self, _val1, _val2, standard_conversions):
        no_error = True
        res_type = 'UNDEF'
        if type(_val1) == np.ndarray:
            res = copy.deepcopy(_val1)
            if type(_val2) == np.ndarray:
                for i in range(min(len(_val1), len(_val2))):
                    res[i] = self.bin_caret(_val1[i], _val2[i], standard_conversions)
            else:
                for i in range(len(_val1)):
                    res[i] = self.bin_caret(_val1[i], _val2, standard_conversions)
            return res
        else:
            if (_val1.type == 'UNDEF') and not (_val2.type == 'UNDEF'):
                _val1.type = _val2.type
            elif (_val2.type == 'UNDEF') and not (_val1.type == 'UNDEF'):
                _val2.type = _val1.type
            elif (_val2.type == 'UNDEF') and (_val1.type == 'UNDEF'):
                return Var()
            x1 = _val1.value
            x2 = _val2.value
            if _val1.type == _val2.type:
                if _val1.type == "NUMERIC":
                    return Var('NUMERIC', x1 ** x2)
                elif _val1.type == "LOGIC":
                    if (x1 is not None) and (x2 is not None):
                        return Var('LOGIC', not (bool(x1) or bool(x2)))
                    else:
                        if (x1 == x2) or (not x1) or (not x2):
                            return Var('LOGIC', None)
                        else:
                            return Var('LOGIC', False)

                elif _val1.type == "STRING":
                    no_error = False
                    sys.stderr.write(f'Illegal operation: type STRING\n')
            else:
                if _val1.left and _val2.right:
                    no_error = False
                    sys.stderr.write(f'Illegal operation: type conversion double definition is illegal\n')
                elif _val1.left:
                    res_type = _val1.type
                    _val1.left = False
                elif _val2.right:
                    res_type = _val2.type
                    _val2.right = False
                else:
                    no_error = False
                    sys.stderr.write(f'Невозможно посчитать, будьте добры указать, куда мне приводить тип\n')
                if no_error:
                    if res_type == "NUMERIC":
                        return Var('NUMERIC',
                                   standard_conversions.converting(_val1, 'NUMERIC').value + standard_conversions.converting(
                                       _val2,
                                       'NUMERIC').value)
                    elif res_type == "LOGIC":
                        x1 = bool(standard_conversions.converting(_val1, 'LOGIC').value)
                        x2 = bool(standard_conversions.converting(_val2, 'LOGIC').value)
                        if (x1 is not None) and (x2 is not None):
                            return Var('LOGIC', not (bool(x1) and bool(x2)))
                        else:
                            if (x1 == x2) or (not x1) or (not x2):
                                return Var('LOGIC', None)
                            else:
                                return Var('LOGIC', False)
                    elif res_type == "STRING":
                        sys.stderr.write(f'Illegal operation: type STRING\n')

    def bin_greater(self, _val1, _val2, standard_conversions):
        no_error = True
        res_type = 'LOGIC'
        if type(_val1) == np.ndarray:
            res = copy.deepcopy(_val1)
            if type(_val2) == np.ndarray:
                for i in range(min(len(_val1), len(_val2))):
                    res[i] = self.bin_greater(_val1[i], _val2[i], standard_conversions)
            else:
                for i in range(len(_val1)):
                    res[i] = self.bin_greater(_val1[i], _val2, standard_conversions)
            return res
        else:
            if (_val1.type == 'UNDEF') and not (_val2.type == 'UNDEF'):
                _val1.type = _val2.type
            elif (_val2.type == 'UNDEF') and not (_val1.type == 'UNDEF'):
                _val2.type = _val1.type
            elif (_val2.type == 'UNDEF') and (_val1.type == 'UNDEF'):
                return Var()
            x1 = _val1.value
            x2 = _val2.value
            if _val1.type == _val2.type:
                return Var('LOGIC', x1 > x2)
            else:
                if _val1.left and _val2.right:
                    no_error = False
                    sys.stderr.write(f'Illegal operation: type conversion double definition is illegal\n')
                elif _val1.left:
                    res_type = _val1.type
                    _val1.left = False
                elif _val2.right:
                    res_type = _val2.type
                    _val2.right = False
                else:
                    no_error = False
                    sys.stderr.write(f'Невозможно посчитать, будьте добры указать, куда мне приводить тип\n')
                if no_error:
                    return Var('LOGIC',
                               standard_conversions.converting(_val1, res_type).value > standard_conversions.converting(_val2,
                                                                                                                res_type).value)

    def bin_less(self, _val1, _val2, standard_conversions):
        no_error = True
        res_type = 'LOGIC'
        if type(_val1) == np.ndarray:
            res = copy.deepcopy(_val1)
            if type(_val2) == np.ndarray:
                for i in range(min(len(_val1), len(_val2))):
                    res[i] = self.bin_less(_val1[i], _val2[i], standard_conversions)
            else:
                for i in range(len(_val1)):
                    res[i] = self.bin_less(_val1[i], _val2, standard_conversions)
            return res
        else:
            if (_val1.type == 'UNDEF') and not (_val2.type == 'UNDEF'):
                _val1.type = _val2.type
            elif (_val2.type == 'UNDEF') and not (_val1.type == 'UNDEF'):
                _val2.type = _val1.type
            elif (_val2.type == 'UNDEF') and (_val1.type == 'UNDEF'):
                return Var()
            x1 = _val1.value
            x2 = _val2.value
            if _val1.type == _val2.type:
                return Var('LOGIC', x1 < x2)
            else:
                if _val1.left and _val2.right:
                    no_error = False
                    sys.stderr.write(f'Illegal operation: type conversion double definition is illegal\n')
                elif _val1.left:
                    res_type = _val1.type
                    _val1.left = False
                elif _val2.right:
                    res_type = _val2.type
                    _val2.right = False
                else:
                    no_error = False
                    sys.stderr.write(f'Невозможно посчитать, будьте добры указать, куда мне приводить тип\n')
                if no_error:
                    return Var('LOGIC',
                               standard_conversions.converting(_val1, res_type).value < standard_conversions.converting(_val2,
                                                                                                                res_type).value)

    def bin_equal(self, _val1, _val2, standard_conversions):
        no_error = True
        res_type = 'LOGIC'
        if type(_val1) == list:
            _val1 = _val1[1]
            res = copy.deepcopy(_val1)
            if type(_val2) == list:
                _val2 = _val2[1]
                for i in range(min(len(_val1), len(_val2))):
                    res[i] = self.bin_equal(_val1[i], _val2[i], standard_conversions)
            else:
                for i in range(len(_val1)):
                    res[i] = self.bin_equal(_val1[i], _val2, standard_conversions)
            return res
        else:
            if (_val1.type == 'UNDEF') and not (_val2.type == 'UNDEF'):
                _val1.type = _val2.type
            if (_val2.type == 'UNDEF') and not (_val1.type == 'UNDEF'):
                _val2.type = _val1.type
            if (_val2.type == 'UNDEF') and (_val1.type == 'UNDEF'):
                return Var()
            x1 = _val1.value
            x2 = _val2.value
            if _val1.type == _val2.type:
                return Var('LOGIC', x1 == x2)
            else:
                if _val1.left and _val2.right:
                    no_error = False
                    sys.stderr.write(f'Illegal operation: type conversion double definition is illegal\n')
                elif _val1.left:
                    res_type = _val1.type
                    _val1.left = False
                elif _val2.right:
                    res_type = _val2.type
                    _val2.right = False
                else:
                    no_error = False
                    sys.stderr.write(f'Невозможно посчитать, будьте добры указать, куда мне приводить тип\n')
                if no_error:
                    return Var('LOGIC',
                               standard_conversions.converting(_val1, res_type).value == standard_conversions.converting(_val2,
                                                                                                                 res_type).value)

    def bin_not_equal(self, _val1, _val2, standard_conversions):
        no_error = True
        res_type = 'LOGIC'
        if type(_val1) == np.ndarray:
            res = copy.deepcopy(_val1)
            if type(_val2) == np.ndarray:
                for i in range(min(len(_val1), len(_val2))):
                    res[i] = self.bin_not_equal(_val1[i], _val2[i], standard_conversions)
            else:
                for i in range(len(_val1)):
                    res[i] = self.bin_not_equal(_val1[i], _val2, standard_conversions)
            return res
        else:
            if (_val1.type == 'UNDEF') and not (_val2.type == 'UNDEF'):
                _val1.type = _val2.type
            if (_val2.type == 'UNDEF') and not (_val1.type == 'UNDEF'):
                _val2.type = _val1.type
            if (_val2.type == 'UNDEF') and (_val1.type == 'UNDEF'):
                return Var()
            x1 = _val1.value
            x2 = _val2.value
            if _val1.type == _val2.type:
                return Var('LOGIC', x1 != x2)
            else:
                if _val1.left and _val2.right:
                    no_error = False
                    sys.stderr.write(f'Illegal operation: type conversion double definition is illegal\n')
                elif _val1.left:
                    res_type = _val1.type
                    _val1.left = False
                elif _val2.right:
                    res_type = _val2.type
                    _val2.right = False
                else:
                    no_error = False
                    sys.stderr.write(f'Невозможно посчитать, будьте добры указать, куда мне приводить тип\n')
                if no_error:
                    return Var('LOGIC',
                               standard_conversions.converting(_val1, res_type).value != standard_conversions.converting(_val2,
                                                                                                                 res_type).value)
