def get_linkedin_prompt(input_blog_keywords, input_linkedin_type, input_linkedin_length, input_linkedin_language, serp_results):
    """
    Generates the prompt for LinkedIn post creation.

    Args:
        input_blog_keywords (str): Keywords for the post.
        input_linkedin_type (str): Type of LinkedIn post.
        input_linkedin_length (str): Length of the post (not used in prompt).
        input_linkedin_language (str): Language for the post.
        serp_results: Search results to include.

    Returns:
        str: The formatted prompt.
    """
    return f"""You are a professional LinkedIn content writer and SEO expert. Your task is to create a detailed, engaging, and SEO-optimized LinkedIn post based on the provided inputs.

### Guidelines:
1. **Title**: Write a concise, keyword-rich title (8-12 words) that grabs attention and clearly conveys the blog's main topic.
2. **Introduction**: Start with an engaging introduction that tells the reader what they will learn or gain from the post. Ensure the introduction also acts as a concise, keyword-rich description for SEO purposes.
3. **Content Structure**:
   - Use clear sections with headings: Title, Introduction, Key Features/Benefits, FAQs (if applicable), and Conclusion.
   - Ensure the content is scannable with bullet points or numbered lists where appropriate.
4. **SEO Optimization**:
   - Incorporate the provided keywords naturally throughout the post.
   - Include actionable insights, examples, or tips to make the content valuable and engaging.
   - Link to credible sources or additional resources where relevant.
5. **Tone and Style**:
   - Maintain a professional yet conversational tone suitable for LinkedIn's audience.
   - Use short, concise sentences for better readability.
   - For technical or niche topics, ensure the content includes sufficient depth and uses an appropriate tone.
6. **Call-to-Action (CTA)**: End with a strong CTA that encourages engagement (e.g., comments, shares, or visiting a link).
7. **Language**: Write the post in the specified language: {input_linkedin_language}.
8. **Post Type**: Tailor the content to the specified post type: {input_linkedin_type}.
9. **Visuals**: Suggest adding relevant visuals (e.g., images, infographics) to enhance engagement.

### Inputs:
- **Blog Keywords**: '{input_blog_keywords}'
- **Google SERP Results**: '{serp_results}'

Generate a LinkedIn post that is professional, engaging, and optimized for both LinkedIn and Google SEO while adhering to the above guidelines."""