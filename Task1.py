from langchain_openai import ChatOpenAI, OpenAIEmbeddings  # Updated imports
from langchain.agents import AgentExecutor, Tool, create_react_agent
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
import os
from dotenv import load_dotenv

load_dotenv()


class PDFQASystem:
    def __init__(self):
        # Updated initialization with new package paths
        self.llm = ChatOpenAI(
            temperature=0,
            model="gpt-3.5-turbo",
            openai_api_key=os.getenv("OPENAI_API_KEY")  # Explicit API key
        )
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        self.active_agents = {}

        self.system_prompt = """You're a PDF analysis expert. Use:
        {tools}

        Response format:
        Thought: {agent_scratchpad}
        Answer: [concise response]"""

    def _create_agent_executor(self, pdf_path: str):
        """Create agent with modern tool setup"""
        try:
            # Load document
            loader = PyPDFLoader(pdf_path)
            pages = loader.load_and_split()

            # Create retriever
            vectorstore = FAISS.from_documents(pages, self.embeddings)
            retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

            # Define tool
            pdf_tool = Tool(
                name="pdf_qa_system",
                func=lambda q: str(retriever.get_relevant_documents(q)),
                description="Searches PDF content for answers"
            )

            # Create agent
            agent = create_react_agent(
                llm=self.llm,
                tools=[pdf_tool],
                prompt=PromptTemplate.from_template(self.system_prompt)
            )

            return AgentExecutor(
                agent=agent,
                tools=[pdf_tool],
                memory=ConversationBufferMemory(),
                handle_parsing_errors=True,  # Better error handling
                verbose=True
            )

        except Exception as e:
            print(f"Agent creation failed: {e}")
            raise

    def process_query(self, pdf_path: str, query: str) -> str:
        """Modern query handling"""
        try:
            filename = os.path.basename(pdf_path)
            if filename not in self.active_agents:
                self.active_agents[filename] = self._create_agent_executor(pdf_path)

            result = self.active_agents[filename].invoke({"input": query})
            return result.get("output", "No answer generated")

        except Exception as e:
            print(f"Query processing error: {e}")
            return f"Error processing query: {str(e)}"


# Singleton instance
pdf_qa_system = PDFQASystem()