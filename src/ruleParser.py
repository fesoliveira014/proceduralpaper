import common

class Parser():
    def __init__(self, rulePath = None):
        self.ruleset = {}
        if not rulePath == None:
            with open(rulePath, "r") as f:
                if f == None:
                    print("Cannot open file " + rulePath)
                    print()
                    return
                for line in f:
                    if len(line) < 3:
                        continue

                    rule = common.Rule()
                    pos = line.find("->")
                    
                    key = line[:pos-1]
                    key = key.strip(" \t\n\r")

                    ruleBody = line[pos+3:len(line)-1]
                    ruleBody.strip(" \t\n\r")

                    pos = ruleBody.find("(")
                    if(pos == -1):
                        rule.childName.append(ruleBody)
                    else:
                        rule.name = ruleBody[:pos]
                        parameters = ruleBody[pos+1 : ruleBody.find(")")]
                        tokens = parameters.split(",")

                        for token in tokens:
                            rule.parameters.append(token)

                        pos = ruleBody.find("{")

                        if not pos == -1:
                            children = ruleBody[pos+1 : ruleBody.find("}")]
                            children.replace("\n", "")
                            tokens = children.split("|")

                            for token in tokens:
                                rule.childName.append(token)

                        pos = ruleBody.find(":")

                        if not pos == -1:
                            rule.probability = float(ruleBody[pos+1:])
                    
                    if not key in self.ruleset:
                        rules = [rule]
                        self.ruleset[key] = rules
                    else:
                        self.ruleset[key].append(rule)
        

    def printRuleset(self):
        for key, rules in self.ruleset.items():
            print("Key: " + key)
            for rule in rules:
                rule.printRule()
            print("----------------------------------")






