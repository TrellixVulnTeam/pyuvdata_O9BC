import uvdata.parameter as uvp


class UVBase(object):

    def __init__(self):
        # set any UVParameter attributes to be properties
        for p in self.parameter_iter():
            this_param = getattr(self, p)
            attr_name = this_param.name
            setattr(self.__class__, attr_name, property(self.prop_fget(p), self.prop_fset(p)))

    def prop_fget(self, param_name):
        def fget(self):
            this_param = getattr(self, param_name)
            return this_param.value
        return fget

    def prop_fset(self, param_name):
        def fset(self, value):
            this_param = getattr(self, param_name)
            this_param.value = value
            setattr(self, param_name, this_param)
        return fset

    def parameter_iter(self):
        attribute_list = [a for a in dir(self) if not a.startswith('__') and
                          not callable(getattr(self, a))]
        param_list = []
        for a in attribute_list:
            attr = getattr(self, a)
            if isinstance(attr, uvp.UVParameter):
                param_list.append(a)
        for a in param_list:
            yield a

    def required_parameter_iter(self):
        attribute_list = [a for a in dir(self) if not a.startswith('__') and
                          not callable(getattr(self, a))]
        required_list = []
        for a in attribute_list:
            attr = getattr(self, a)
            if isinstance(attr, uvp.UVParameter):
                if attr.required:
                    required_list.append(a)
        for a in required_list:
            yield a

    def extra_parameter_iter(self):
        attribute_list = [a for a in dir(self) if not a.startswith('__') and
                          not callable(getattr(self, a))]
        extra_list = []
        for a in attribute_list:
            attr = getattr(self, a)
            if isinstance(attr, uvp.UVParameter):
                if not attr.required:
                    extra_list.append(a)
        for a in extra_list:
            yield a

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            # only check that required parameters are identical
            isequal = True
            for p in self.required_parameter_iter():
                self_param = getattr(self, p)
                other_param = getattr(other, p)
                if self_param != other_param:
                    # print('parameter {pname} does not match. Left is {lval} '
                    #       'and right is {rval}'.
                    #       format(pname=p, lval=str(self_param.value),
                    #              rval=str(other_param.value)))
                    isequal = False
            return isequal
        else:
            print('Classes do not match')
            return False

    def __ne__(self, other):
        return not self.__eq__(other)
