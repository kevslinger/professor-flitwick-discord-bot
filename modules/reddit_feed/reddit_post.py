class RedditPost:
	def __init__(self, bot, post):
		self.bot = bot
		self.post = post

	def process_post(self):
		"""check post and announce if not saved"""
		# log post details in console
		print(f"Recieved post by {self.post.author}")
		# create message with url and text
		title, message = self.__build_message()
		return self.post.subreddit, title, self.post.author, message

	def __trim_text(self, text, limit=97):
		"""trim text if over limit of characters"""
		if len(text) > limit:
			# trim text if over limit of characters
			return text[:limit] + "..."
		# otherwise, return original
		return text

	def __build_message(self):
		"""build message from post"""
		# get url and selftext
		title = self.__trim_text(self.post.title)
		url = f"https://redd.it/{self.post.id}"
		return title, url


async def check_livegame_comment(comment) -> bool:
	sub = comment.subreddit
	parent_post = await comment.parent()
	top_level = str(comment.link_id)[3:] == str(parent_post)
	mods = [mod for mod in await sub.moderator()]
	is_mod = comment.author in mods

	if top_level and is_mod and "The Live Game is OVER" in comment.body:
		return True
	return False

