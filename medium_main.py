import medium_story
import google_doc
import llm
from prompts_library import medium_prompts

#service = "Cohere"
#model = "command"

service = "OpenAI"
model = "gpt-3.5-turbo"

# Ask the user for the YouTube link
youtube_link = input("Enter the YouTube video link: ")

# Extract the video ID from the link (assuming standard YouTube URL)
video_id = youtube_link.split("v=")[1]

# Extract the video transcript
transcript = medium_story.get_video_transcript(video_id)
if transcript:
    print("Transcript exists.")
else:
    print("No transcript available.")

prompt = medium_prompts.medium_story_prompt.format(video_script = transcript)
# blog_post = medium_story.generate_blog_post(transcript)
blog_post = llm.llm_generate_text(prompt,service,model)
print("Blog Post Generated")

# Generate the title for the blog post
doc_title = medium_story.generate_title(blog_post)

# Create Google Doc
google_doc.create_google_doc(doc_title, blog_post)