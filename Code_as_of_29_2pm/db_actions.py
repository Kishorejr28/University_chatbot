from sqlalchemy import create_engine, Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import uuid

# Database setup
DATABASE_URL = "sqlite:///chat_history.db"
Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ChatHistory model
class ChatHistory(Base):
    __tablename__ = 'chat_history'
    
    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(String, unique=True, index=True)
    history = Column(JSON)  # Store chat history as JSON

# Create tables
Base.metadata.create_all(bind=engine)

# Function to create a new chat ID and initialize history
def create_chat_id():
    session = SessionLocal()
    try:
        chat_id = str(uuid.uuid4())  # Generate a unique chat_id
        new_chat = ChatHistory(chat_id=chat_id, history=[])
        session.add(new_chat)
        session.commit()
        print(f"Created new chat with ID: {chat_id}")  # Debugging print
        return chat_id
    except Exception as e:
        session.rollback()
        print("Error in creating chat ID:", e)  # Debugging print
        raise e
    finally:
        session.close()

def update_chat_history(chat_id: str, question: str, context: str, response: str,model_choice:str,frame_work_used:str):
    session = SessionLocal()
    try:
        # Fetch the chat history entry
        chat = session.query(ChatHistory).filter(ChatHistory.chat_id == chat_id).first()

        # print(chat.history if chat else "No chat found", "History before commit")

        if chat:
            # Ensure history is a list
            if not isinstance(chat.history, list):
                chat.history = []
        else:
            # Create a new chat if it doesn't exist
            chat = ChatHistory(chat_id=chat_id, history=[])
            session.add(chat)

        # Append the new chat interaction to the history
        new_entry = {
            'Question': question,
            'Context': context,
            'Response': response,
            'model': model_choice,
            'frame_work': frame_work_used
        }
        updated_history = chat.history + [new_entry]  # Create new list with appended entry
        chat.history = updated_history  # Assign back the updated list to chat.history

        # print("Appending new entry:", new_entry)
        # print("Updated history:", updated_history)

        # Flush and commit changes to the database
        session.commit()
        print(f"Successfully committed changes for chat_id: {chat_id}")
    except Exception as e:
        session.rollback()
        print("Error occurred during update:", e)
        raise e
    finally:
        session.close()



def get_history_by_id(chat_id: str):
    session = SessionLocal()
    try:
        chat = session.query(ChatHistory).filter(ChatHistory.chat_id == chat_id).first()

        # Debug: Check if the chat exists
        if not chat:
            print(f"No chat history found for chat_id: {chat_id}")
            return None

        # Ensure the history is returned as a list
        if not isinstance(chat.history, list):
            print(f"History for chat_id {chat_id} is not a list, resetting to empty list")
            return []

        # print(f"Retrieved history for chat_id {chat_id}: {chat.history}")  # Debugging print
        return chat.history
    except Exception as e:
        print("Error in retrieving history:", e)  # Debugging print
        raise e
    finally:
        session.close()

def get_all_chat_history():
    session = SessionLocal()
    try:
        chats = session.query(ChatHistory).all()
        all_history = []
        
        # Debugging: Check the raw chats fetched from the database
        print("Raw chats from database:", chats)  # Debugging print

        # Convert each chat record into a dictionary
        for chat in chats:
            all_history.append({
                'chat_id': chat.chat_id,
                'history': chat.history
            })
        
        # print("Retrieved all chat history:", all_history)  # Debugging print
        return all_history
    except Exception as e:
        print("Error in retrieving all chat history:", e)  # Debugging print
        raise e
    finally:
        session.close()

def get_last_n_chat_history(n=3):
    session = SessionLocal()
    try:
        # Fetch the last n chat history entries ordered by ID (assuming ID is auto-incremented)
        chats = session.query(ChatHistory).order_by(ChatHistory.id.desc()).limit(n).all()
        
        last_chat_history = []
        
        # Convert each chat record into a dictionary
        for chat in chats:
            last_chat_history.append({
                'chat_id': chat.chat_id,
                'history': chat.history
            })
        
        # print(f"Retrieved the last {n} chat history:", last_chat_history)  # Debugging print
        return last_chat_history
    except Exception as e:
        print("Error in retrieving last chat history:", e)  # Debugging print
        raise e
    finally:
        session.close()


def get_recent_lang_chats(limit=3):
    session = SessionLocal()
    try:
        # Retrieve all chat histories
        all_chats = session.query(ChatHistory).all()

        lang_chats = []

        # Loop through each chat's history to find entries where frame_work == 'lang'
        for chat in all_chats:
            if isinstance(chat.history, list):
                for entry in chat.history:
                    if entry.get('frame_work') == 'lang':
                        lang_chats.append({
                            'chat_id': chat.chat_id,
                            'Question': entry['Question'],
                            'Context': entry['Context'],
                            'Response': entry['Response'],
                            'model': entry['model'],
                            'frame_work': entry['frame_work']
                        })

        # Sort by recent entries (assuming they were appended chronologically)
        lang_chats = sorted(lang_chats, key=lambda x: x['chat_id'], reverse=True)

        # Return the most recent 3 entries
        return lang_chats[:limit]

    except Exception as e:
        print("Error in retrieving recent 'lang' framework chats:", e)
        raise e
    finally:
        session.close()


def get_recent_lang_chats(limit=3):
    session = SessionLocal()
    try:
        # Retrieve all chat histories
        all_chats = session.query(ChatHistory).all()

        lang_chats = []

        # Loop through each chat's history to find entries where frame_work == 'lang'
        for chat in all_chats:
            if isinstance(chat.history, list):
                for entry in chat.history:
                    if entry.get('frame_work') == 'lang':
                        lang_chats.append({
                            'chat_id': chat.chat_id,
                            'Question': entry['Question'],
                            'Context': entry['Context'],
                            'Response': entry['Response'],
                            'model': entry['model'],
                            'frame_work': entry['frame_work']
                        })

        # Sort by recent entries (assuming they were appended chronologically)
        lang_chats = sorted(lang_chats, key=lambda x: x['chat_id'], reverse=True)

        # Return the most recent 3 entries
        return lang_chats[:limit]

    except Exception as e:
        print("Error in retrieving recent 'lang' framework chats:", e)
        raise e
    finally:
        session.close()


def get_recent_llama_chats(limit=3):
    session = SessionLocal()
    try:
        # Retrieve all chat histories
        all_chats = session.query(ChatHistory).all()

        lang_chats = []

        # Loop through each chat's history to find entries where frame_work == 'llama'
        for chat in all_chats:
            if isinstance(chat.history, list):
                for entry in chat.history:
                    if entry.get('frame_work') == 'llama':
                        lang_chats.append({
                            'chat_id': chat.chat_id,
                            'Question': entry['Question'],
                            'Context': entry['Context'],
                            'Response': entry['Response'],
                            'model': entry['model'],
                            'frame_work': entry['frame_work']
                        })

        # Sort by recent entries (assuming they were appended chronologically)
        lang_chats = sorted(lang_chats, key=lambda x: x['chat_id'], reverse=True)

        # Return the most recent 3 entries
        return lang_chats[:limit]

    except Exception as e:
        print("Error in retrieving recent 'llama' framework chats:", e)
        raise e
    finally:
        session.close()