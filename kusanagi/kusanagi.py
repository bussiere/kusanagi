import wsgiref.handlers
import os
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext import db

class Graph:
    def __init__(self,name):
        self.name = name
        self.list_neighbor = {}
        self.list_node = {}
    def add_node(self,node):
        self.list_node[node] = True

    def add_edge(self,node,nodebis):
        try :
            self.list_neighbor[node].append(nodebis)
        except :
            self.list_neighbor[node] = []
            self.list_neighbor[node].append(nodebis)
        try :
            self.list_neighbor[nodebis].append(node)
        except :
            self.list_neighbor[nodebis] = []
            self.list_neighbor[nodebis].append(node)
    def neighbors(self,node):
        try :
            return self.list_neighbor[node]
        except :
            return []
    def nodes(self):
        return self.list_node.keys()
    def delete_edge(self,node,nodebis):
        self.list_neighbor[node].remove(nodebis)
        self.list_neighbor[nodebis].remove(node)
    def delete_node(self,node):
        del self.list_node[node]
        try :
            for nodebis in self.list_neighbor[node] :
                self.list_neighbor[nodebis].remove(node)
            del self.list_neighbor[node]
        except :
            return "error"

class Clerks(db.Model) :
        id = db.IntegerProperty()
        nom = db.StringProperty()
        prenom = db.StringProperty()
        telephone = db.StringProperty()
        email = db.EmailProperty()
        service = db.StringProperty()
        type = 'Clerks'

class Services(db.Model) :
        id = db.IntegerProperty()
        name = db.StringProperty()
        type = 'Services'

class Entreprises(db.Model) :
        id = db.IntegerProperty()
        name = db.StringProperty()
        type = 'Enterprises'

class Speakers(Clerks) :
        entreprise = db.IntegerProperty()
        type = 'Speakers'

class Interventions(db.Model) :
        id = db.IntegerProperty()
        datedebut =db.DateTimeProperty()
        datefin = db.DateTimeProperty()
        statut= "Open"
        note = ""
        clerks = []
        speakers = []
        description = []
        type = 'Interventions'

class Descriptions(db.Model) :
        id = db.IntegerProperty()
        text = ""
        type = 'Descriptions'


class App :
    def __init__(self,urllogout):

        self.Nom_Intervention = "Intervention"
        self.Lien_Intervention = "../" + self.Nom_Intervention + "/"
        self.Nom_InterventionA = "Ajouter Intervention"
        self.Lien_InterventionA = "../" + self.Nom_Intervention + "/?cmd=ajout"
        self.Nom_InterventionE = "Editer Intervention"
        self.Lien_InterventionE = "../" + self.Nom_Intervention + "/?cmd=edit"
        self.Nom_Personnes = "Personnes"
        self.Lien_Personnes = "../" +self.Nom_Personnes + "/"
        self.Nom_PersonnesAA = "Ajout Agent"
        self.Lien_PersonnesAA = "../" +self.Nom_Personnes + "/?cat=agent&cmd=ajout"
        self.Nom_PersonnesAE = "Edit Agent"
        self.Lien_PersonnesAE = "../" +self.Nom_Personnes + "/?cat=agent&cmd=edit"
        self.Nom_PersonnesIA = "Ajout Intervenant"
        self.Lien_PersonnesIA = "../" +self.Nom_Personnes + "/?cat=intervenant&cmd=ajout"
        self.Nom_PersonnesIE = "Edit Intervenant"
        self.Lien_PersonnesIE = "../" +self.Nom_Personnes + "/?cat=intervenant&cmd=edit"
        self.Nom_Description = "Description"
        self.Lien_Description = "../" +self.Nom_Description + "/"
        self.Nom_DescriptionE = "Description Edit"
        self.Lien_DescriptionE ="../" + self.Nom_Description + "/?cmd=edit"
        self.Nom_DescriptionA = "Description Ajout"
        self.Lien_DescriptionA ="../" + self.Nom_Description + "/?cmd=ajout"
        self.Nom_Logout = "Logout"
        self.Lien_Logout = urllogout

class MainPage(webapp.RequestHandler):
         def get(self):
                 user = users.get_current_user()

                 if user:
                         path = os.path.join(os.path.dirname(__file__), 'templates/base/Menu.html')
                         self.response.headers['Content-Type'] = 'text/html'
                         app = App(users.create_logout_url(self.request.uri))
                         template_values = {
                         'App': app,
                         }
                         self.response.out.write(template.render(path, template_values))

                 else:
                         self.redirect(users.create_login_url(self.request.uri))

def main():

         application = webapp.WSGIApplication([('/', MainPage)],debug=True)
         wsgiref.handlers.CGIHandler().run(application)

if __name__ == "__main__":
         main()