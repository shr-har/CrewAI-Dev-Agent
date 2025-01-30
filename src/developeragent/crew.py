from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai import LLM, Agent, Crew, Process, Task
# from docling_core.types.doc.document import DoclingDocument
# from crewai.knowledge.source.crew_docling_source import CrewDoclingSource
from crewai.knowledge.source.pdf_knowledge_source import PDFKnowledgeSource
# from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource
# print(DoclingDocument)


# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators
# Create a knowledge source
content_source = PDFKnowledgeSource(
    file_paths=[
    "Detailed_FastAPI_Guide.pdf",
    ],
)
# Create an LLM with a temperature of 0 to ensure deterministic outputs
llm = LLM(model="gpt-4o-mini", temperature=0)
@CrewBase
class CrewaiDeveloperagent():
	"""CrewaiDeveloperagent crew"""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools
	@agent
	def developer(self) -> Agent:
		return Agent(
			config=self.agents_config['developer'],
			verbose=True,
			allow_delegation=False,
    		llm=llm,
		)

	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task
	@task
	def development_task(self) -> Task:
		return Task(
			config=self.tasks_config['development_task'],
			output_file='report.md'
		)

	# @task
	# def debugging_task(self) -> Task:
	# 	return Task(
	# 		config=self.tasks_config['debugging_task'],
	# 		output_file='report.md'
	# 	)

	@crew
	def crew(self) -> Crew:
		"""Creates the CrewaiDeveloperagent crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			knowledge_sources=[content_source]
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
