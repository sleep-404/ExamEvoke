from .batch import BatchViewset
from .course import CourseViewset
from .organization import OrganizationViewset
from .subject import SubjectViewset
from .topic import TopicViewset
# from ..user.employee import EmployeeViewset

__all__ = [
    "CourseViewset",
    "BatchViewset",
    "OrganizationViewset",
    "SubjectViewset",
    "TopicViewset",
]
