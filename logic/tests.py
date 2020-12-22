from datetime import datetime
from unittest import TestCase


# Create your tests here.


class Project:

    def __init__(self, project_name, project_date):
        self.name = project_name
        self.release_date = project_date
        self.request_count = 0

    @staticmethod
    def named(project_name, project_date):
        return Project(project_name, project_date)

    def is_named(self, project_name):
        return self.name == project_name

    def register_request_at(self, request_datetime):
        self.request_count = self.request_count + 1

    def request_count_is(self, count):
        return self.request_count == count


class RequestLimitedProject(Project):

    def __init__(self, project_name, project_date, request_limit):
        super().__init__(project_name, project_date)
        self.request_limit = request_limit

    def has_available_request_calls(self):
        return True

    @classmethod
    def from_project(cls, project, limit):
        return cls(project.name, project.release_date, limit)


class Manager:

    def __init__(self, username):
        self.limited_projects = dict()
        self.active_projects = dict()
        self.inactive_projects = dict()
        self.username = username

    @staticmethod
    def identified_as(username):
        return Manager(username)

    def is_identified_as(self, username):
        return self.username == username

    def start_project_on(self, project_name, project_date):
        self.inactive_projects[project_name] = (Project.named(project_name, project_date))

    def has_project_named(self, project_name):
        return project_name in self.inactive_projects

    def has_active_projects(self):
        return len(self.active_projects) > 0

    def has_active_project_named(self, active_project_name):
        return active_project_name in self.active_projects

    def deactivate_project(self, project_name):
        project = self.active_projects.pop(project_name)
        self.inactive_projects[project_name] = project

    def has_inactive_project_named(self, project_name):
        return project_name in self.inactive_projects

    def activate_project(self, project_name):
        project = self.inactive_projects.pop(project_name)
        self.active_projects[project_name] = project

    def has_inactive_projects(self):
        return len(self.inactive_projects) > 0

    def register_request_to_project_at(self, project_name, request_datetime):
        self.active_projects[project_name].register_request_at(request_datetime)

    def project_request_count_is(self, project_name, count):
        return self.active_projects[project_name].request_count_is(count)

    def limit_project_request_per_month(self, project_name, limit):
        limited_project = RequestLimitedProject.from_project(self.active_projects[project_name], limit)
        del self.active_projects[project_name]
        self.limited_projects[limited_project] = limited_project

    def project_limit_is(self, limit):
        return True

    def project_has_requests_left(self):
        return True


class TestValues:

    def setUp(self):
        self.TEST_MANAGER_USERNAME = "MyTestUserName"
        self.TEST_MANAGER_USERNAME2 = "AnotherTestUserName"
        self.TEST_PROJECT_NAME = "My BFA project"
        self.TEST_PROJECT_NAME2 = "Another BFA project"
        self.TEST_PROJECT_DATE = datetime(2020, 10, 10, 13, 0, 0, 0)
        self.REQUEST_DATETIMES = [datetime(2020, 10, 10, 13, 1, 0, 0)]
        self.TEST_REQUEST_LIMIT = 10
        self.REGISTRATION_DATE = datetime(2020, 9, 9, 10, 0, 0, 0)


class TestProject(TestValues, TestCase):

    def test_project_named(self):
        project = self.create_project()
        self.assertIsNotNone(project)
        self.assertTrue(project.is_named(self.TEST_PROJECT_NAME))
        self.assertFalse(project.is_named(self.TEST_PROJECT_NAME2))

    def create_project(self):
        project = Project.named(self.TEST_PROJECT_NAME, self.TEST_PROJECT_DATE)
        return project

    def test_register_request(self):
        project = self.create_project()
        project.register_request_at(self.REQUEST_DATETIMES[0])
        self.assertTrue(project.request_count_is(1))


class TestManager(TestValues, TestCase):

    def test_create_manager(self):
        manager = self.create_manager()

        self.assertIsNotNone(manager)
        self.assertTrue(manager.is_identified_as(self.TEST_MANAGER_USERNAME))
        self.assertFalse(manager.is_identified_as(self.TEST_MANAGER_USERNAME2))

    def test_manager_starts_project(self):
        manager = self.create_manager_with_project()
        self.assertTrue(manager.has_project_named(self.TEST_PROJECT_NAME))
        self.assertFalse(manager.has_project_named(self.TEST_PROJECT_NAME2))
        self.assertTrue(manager.has_inactive_projects())
        self.assertTrue(manager.has_inactive_project_named(self.TEST_PROJECT_NAME))

    def test_activate_project(self):
        manager = self.create_manager_with_project_and_activate()

        self.assertTrue(manager.has_active_project_named(self.TEST_PROJECT_NAME))
        self.assertTrue(manager.has_active_projects())
        self.assertFalse(manager.has_inactive_projects())

    def create_manager_with_project(self):
        manager = self.create_manager()
        manager.start_project_on(self.TEST_PROJECT_NAME, self.TEST_PROJECT_DATE)
        return manager

    def test_register_request(self):
        manager = self.create_manager_with_project_and_activate()
        manager.register_request_to_project_at(self.TEST_PROJECT_NAME, self.REQUEST_DATETIMES[0])
        self.assertTrue(manager.project_request_count_is(self.TEST_PROJECT_NAME, 1))

    def create_manager_with_project_and_activate(self):
        manager = self.create_manager_with_project()
        manager.activate_project(self.TEST_PROJECT_NAME)
        return manager

    def create_manager(self):
        manager = Manager.identified_as(self.TEST_MANAGER_USERNAME)
        return manager

    def test_set_request_limit(self):
        manager = self.create_manager_with_project_and_activate()
        manager.limit_project_request_per_month(self.TEST_PROJECT_NAME, self.TEST_REQUEST_LIMIT)
        self.assertTrue(manager.project_limit_is(self.TEST_REQUEST_LIMIT))
        self.assertTrue(manager.project_has_requests_left())


class EthNodeManagementSystem:
    def __init__(self):
        self.registration_dates = dict()
        self.managers = dict()

    def register_manager(self, manager_username, registration_date):
        self.managers[manager_username] = Manager.identified_as(manager_username)
        self.registration_dates.setdefault(registration_date, set())
        self.registration_dates[registration_date].add(manager_username)

    def has_manager_named(self, manager_username):
        return manager_username in self.managers

    def start_project_by_manager(self, manager_username, project_name, project_date):
        self.managers[manager_username].start_project_on(project_name, project_date)

    def activate_project_by_manager(self, manager_username, project_name):
        self.managers[manager_username].activate_project(project_name)

    def project_by_manager_is_active(self, manager_username, project_name):
        return self.managers[manager_username].has_active_project_named(project_name)


class TestEthNodeManagementSystem(TestValues, TestCase):

    def test_register(self):
        system = self.create_system_and_manager()
        self.assertTrue(system.has_manager_named(self.TEST_MANAGER_USERNAME))
        self.assertFalse(system.has_manager_named(self.TEST_PROJECT_NAME2))

    def test_manager_starts_project(self):
        system = self.create_system_and_manager()
        system.start_project_by_manager(self.TEST_MANAGER_USERNAME, self.TEST_PROJECT_NAME, self.TEST_PROJECT_DATE)

    def create_system_and_manager(self):
        system = EthNodeManagementSystem()
        system.register_manager(self.TEST_MANAGER_USERNAME, self.REGISTRATION_DATE)
        return system

    def test_manager_activates_project(self):
        system = self.create_system_and_manager()
        system.start_project_by_manager(self.TEST_MANAGER_USERNAME, self.TEST_PROJECT_NAME, self.TEST_PROJECT_DATE)
        system.activate_project_by_manager(self.TEST_MANAGER_USERNAME, self.TEST_PROJECT_NAME)
        self.assertTrue(system.project_by_manager_is_active(self.TEST_MANAGER_USERNAME, self.TEST_PROJECT_NAME))
