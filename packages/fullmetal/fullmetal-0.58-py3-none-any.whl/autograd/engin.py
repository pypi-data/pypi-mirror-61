
class autograd(object):
    __slots__ = ('type','t')
    """docstring for autograd."""

    def __init__(self, t):
        super(autograd, self).__init__()
        self.type = type(t)
        self.t = t

    def backward(self, grad: "Node" = None) -> None:
        assert self.t.requires_grad, "called backward on non-requires-grad Node"
        if grad is None:
            if self.t.shape == ():
                grad = self.type(1.0)
            else:
                raise RuntimeError("grad must be specified for non-0-Node")
        self.t.grad.data = self.t.grad.data + grad.data  # type: ignore
        for dependency in self.t.depends_on: #loop over the list
            backward_grad = dependency.grad_fn(grad.data) # apply gard fuction
            dependency.Node.backward(self.type(backward_grad)) # get current Node
                                                                      # apply backward function
                                                                      # wrapping the output gardent
