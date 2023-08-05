import logging
from collections import defaultdict

from orchestra.models import Project
from orchestra.models import Step
from orchestra.models import WorkflowVersion
from orchestra.project_api.serializers import ProjectSerializer
from orchestra.project_api.serializers import TaskSerializer

logger = logging.getLogger(__name__)


class MalformedDependencyException(Exception):
    pass


def get_project_information(project_ids):
    """
    output format:
    { project_id: {
        'project': serialized_project_data,
        'tasks': project_tasks_list,
        'steps': project_workflow_steps
        },
        ...
    }
    Example:
    {
        123: {
            'project': {},
            'tasks': [],
            'steps': []
        },
        ...
    }
    """
    projects = Project.objects.select_related(
        'workflow_version__workflow'
        ).filter(id__in=project_ids).prefetch_related('tasks')
    projects_dict = defaultdict(dict)
    for project in projects:
        project_id = project.id
        workflow_version = project.workflow_version
        workflow = workflow_version.workflow

        projects_dict[project_id]['project'] = ProjectSerializer(
            project).data
        projects_dict[project_id]['steps'] = get_workflow_steps(
            workflow.slug, workflow_version.slug)
        tasks = defaultdict(dict)
        for task in project.tasks.all():
            tasks[project.id][task.step.slug] = TaskSerializer(task).data
        projects_dict[project_id]['tasks'] = tasks.get(project_id, {})
    return projects_dict


def get_workflow_steps(workflow_slug, version_slug):
    """Get a sorted list of steps for a project.

    Arguments:
        workflow_slug (str):
            Unique identifier of the workflow to get steps for.
        version_slug (str):
            identifier for the version of the workflow to get steps for.

    Returns:
        workflow_steps (str):
            A list of (step_slug, step_description) tuples topologically sorted
            so that earlier steps are prerequisites for later ones.
    """
    workflow_version = WorkflowVersion.objects.get(
        slug=version_slug,
        workflow__slug=workflow_slug)

    # Build a directed graph of the step dependencies
    # TODO(dhaas): make DB access more efficient.
    graph = {}
    for step in workflow_version.steps.all():
        graph[step.slug] = [dependency.slug for dependency
                            in step.creation_depends_on.all()]
    return _traverse_step_graph(graph, workflow_version)


def _traverse_step_graph(graph, workflow_version):
    queue = []
    for key, value in graph.items():
        if value == []:
            queue.append(key)

    # TODO(derek): prevent the MalformedDependencyExceptions from being
    # possible by baking protection into the Workflow/Step classes
    if not len(queue):
        raise MalformedDependencyException("All %s workflow steps have "
                                           "dependencies. There is no start "
                                           "point." % workflow_version.slug)

    # Build the steps list in order using a breadth-first-like traversal of the
    # step dependency graph
    steps = []
    already_added = set()
    while len(queue):
        current_node = queue.pop(0)

        if current_node in already_added:
            continue

        # TODO(dhaas): make DB access more efficient (one option: cache steps
        # in the graph).
        already_added.add(current_node)
        current_step = Step.objects.get(
            workflow_version=workflow_version,
            slug=current_node)
        steps.append({'slug': current_node,
                      'description': current_step.description,
                      'is_human': current_step.is_human,
                      'name': current_step.name})

        for key, dependencies in graph.items():
            if (current_node in dependencies and
                    key not in already_added):
                queue.append(key)

    return steps
