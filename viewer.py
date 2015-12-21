# coding=cp1251
import pefile


class Viewer(object):
    def __init__(self, path, learn=False):
        self.pe = pefile.PE(path)
        self.path = path
        self.learn_result = {"Functions": []}
        self.learn = learn

    def get_learned_result(self):
        return self.learn_result

    def search_imports(self, functions):
        search_set = set()
        search_map = {}
        result = []
        if not hasattr(self.pe, 'DIRECTORY_ENTRY_IMPORT'):
            print (u"Отсутствует таблица "
                   u"импорта: %s" % self.path[self.path.rindex("\\") + 1:])
            return

        for module in self.pe.DIRECTORY_ENTRY_IMPORT:
            for imports in module.imports:
                if imports.name is not None:
                    search_set.add((imports.name, None))
                if imports.ordinal is not None:
                    search_set.add((None, imports.ordinal))
                if imports.name is not None and imports.ordinal is not None:
                    search_set.add((imports.name, imports.ordinal))
                    search_map.update({imports.name: imports.ordinal})
                    search_map.update({imports.ordinal: imports.name})

        for func in functions:
            if func.get("Snippet"):
                for item in search_set:
                    name, ordinal = item
                    snippet = func.get("Snippet")
                    if name is not None and snippet in name:
                        result.append((self.path, name, ordinal))
                    elif ordinal is not None and snippet in str(ordinal):
                        result.append((self.path, name, ordinal))
                continue
            entry = (func.get("Name"), func.get("Ordinal"))
            if entry in search_set:
                result.append((self.path, func.get("Name"),
                               func.get("Ordinal")))
                if self.learn:
                    if func.get("Name") is not None:
                        self.learn_result["Functions"].append({
                            "Name": func.get("Name"),
                            "Ordinal": search_map.get(func.get("Name"))})
                    elif func.get("Ordinal") is not None:
                        self.learn_result["Functions"].append({
                            "Name": search_map.get(func.get("Ordinal")),
                            "Ordinal": func.get("Ordinal")})
        return result
