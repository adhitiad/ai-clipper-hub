import time
import sys
from unittest.mock import patch, MagicMock

# Mock dependencies before importing engagement
sys.modules['database'] = MagicMock()
import database
database.db = MagicMock()

sys.modules['langchain_groq'] = MagicMock()
sys.modules['config'] = MagicMock()
sys.modules['logger'] = MagicMock()

from engagement import reply_to_new_comments

def run_benchmark():
    # Setup mocks
    mock_db = database.db
    # Mock active_videos
    mock_db.published_clips.find.return_value.sort.return_value.limit.return_value = [
        {"niche": f"niche_{i}"} for i in range(5)
    ]

    # Mock comments - 3 per niche
    def mock_find(query):
        mock_cursor = MagicMock()
        mock_cursor.limit.return_value = [
            {"_id": f"comment_{query['niche']}_{j}", "text": f"text {j}", "niche": query['niche']}
            for j in range(3)
        ]
        # Simulate network latency
        time.sleep(0.05)
        return mock_cursor

    mock_db.raw_comments.find.side_effect = mock_find

    # Mock update_one
    def mock_update(*args, **kwargs):
        time.sleep(0.05)
    mock_db.raw_comments.update_one.side_effect = mock_update
    mock_db.raw_comments.bulk_write.side_effect = lambda *args, **kwargs: time.sleep(0.05)

    # Mock LLM
    mock_llm_instance = MagicMock()
    def mock_invoke(*args, **kwargs):
        time.sleep(0.5) # Simulate LLM latency
        mock_resp = MagicMock()
        mock_resp.content = "mocked reply"
        return mock_resp

    def mock_batch(prompts, *args, **kwargs):
        time.sleep(0.5) # Simulate LLM batch latency
        return [MagicMock(content="mocked reply") for _ in prompts]

    mock_llm_instance.invoke.side_effect = mock_invoke
    mock_llm_instance.batch.side_effect = mock_batch

    with patch('engagement.ChatGroq', return_value=mock_llm_instance):
        start = time.time()
        reply_to_new_comments()
        end = time.time()

    print(f"Execution time: {end - start:.2f} seconds")

if __name__ == "__main__":
    run_benchmark()
