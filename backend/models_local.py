import image as image

class Artist:
    def __init__(self, id="tmp", genome="tmp", generation=0, member=0, fitness="None",
                 father="None", mother="None", rank=None):
        self.id = id
        self.genome = genome
        self.fitness = fitness
        self.generation = generation
        self.member = member
        self.father = father  # またはNone
        self.mother = mother  # またはNone
        self.rank = rank      # トーナメントでの順位

    # id
    def __str__(self):
        return "g{0}_m{1}".format(self.generation, self.member)

    def function(self):
        return image.print_gene(self.genome, 0, 1)
