from . import search_request as sr

import requests
from bs4 import BeautifulSoup

# Usage: s = LibgenSearch()
# 		 s.title_search("lord of the rings")

class LibgenSearch:

	def title_search(self, query, language="", file_format=""):
		self.query = query
		self.language = language
		self.file_format = file_format
		self.search_request = sr.SearchRequest(query, search_type="title")
		return self.search_request.aggregate_request_data()

	def author_search(self, query, language="", file_format=""):
		self.query = query
		self.language = language
		self.file_format = file_format
		self.search_request = sr.SearchRequest(query, search_type="author")
		return self.search_request.aggregate_request_data()

