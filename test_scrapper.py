import fonctions as fn
import unittest


###############################################################################################
#   Bonjour Monsieur, vous risquez de trouver des warming dans le code. En effet, j'ai des    #
#   erreur de webscotter et pyppeteer que je n'ai pas réussi à régler. Ca m'affiche des       #
#   WARMING mais le code fonctionne                                                           #
###############################################################################################


class TestClass:
    
    input_file = "input.json"
    soup = fn.get_soup("fmsoym8I-3o")

    # s'assurer que la connexion est établie affiche 200 
    def test_get_page(self):
        f = fn.get_page("input.json")
        assert f == 200
    
    def test_json_to_dataframe(self):
        df_function = fn.json_to_dataframe(self.input_file)
        assert df_function.loc[0,"videos_id"] == "fmsoym8I-3o"
        assert df_function.loc[1,"videos_id"] == "JhWZWXvN_yo" 
    
    def test_title_of_video(self):
        f = fn.title_of_video(self.soup)
        assert f == "Pierre Niney : L’interview face cachée par HugoDécrypte - YouTube"
    
    def test_videaste_of_video(self):
        f = fn.videaste_of_video(self.soup)
        assert f == "HugoDécrypte"

    def test_videoId_of_video(self):
        assert fn.videoId_of_video(self.soup) == "fmsoym8I-3o"

    def test_likes_of_video(self):
        assert int(fn.likes_of_video(self.soup)) >= 0

    def test_description_url_of_video(self):
        assert fn.description_url_of_video(self.soup) == []