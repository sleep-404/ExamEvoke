from .students.viewsets import (
    StudentViewset,
)

from .users.viewsets import (
    EmployeeViewset,
    CustomAuthTokenView,
)


__all__ = [
    "StudentViewset",
    "EmployeeViewset",
    "CustomAuthTokenView",
]