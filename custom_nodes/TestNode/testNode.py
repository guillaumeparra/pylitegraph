
class TestNode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "myString": ("STRING", {"forceInput": True}),
                "MyDropDownMenu": (["action01", "action02"], {}),
            },
            "optional": {
                "myOptionalText": ("STRING", {"default":"toto", "multiline": False, "dynamicPrompts": False}),
                "myImage": ("IMAGE",),
                "myInt": ("INT", {
                    "default": 0, 
                    "min": 0, # Minimum value
                    "max": 4096, # Maximum value
                    "step": 64, # Slider's step
                    "display": "number" # Cosmetic only: display as "number" or "slider"
                }),
                "myFloat": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 10.0,
                    "step": 0.01,
                    "round": 0.001, # The value representing the precision to round to, will be set to the step value by default. Can be set to False to disable rounding.
                    "display": "number"}),

                "myToggle": ("TOGGLE"),
                },
        }

    # le type des output
    RETURN_TYPES = ("STRING",)

    # nom de la fonction qui va s'executer et qui est determinee a continuation
    FUNCTION = "myFunction"

    # va determiner si le node peut etre execute en fin de chaine
    OUTPUT_NODE = True

    # endroit ou est range le node dans le menu accessible via clic droit dans l'interface
    CATEGORY = "TestCategory"

    # permet de flaguer si le node doit etre detecte comme etant une finalite dans le graph

    def myFunction(self, myString, MyDropDownMenu, myOptionalText="", myImage=None, myInt=1, myFloat=0.0, myToggle=True):

        r = "%s_%s_%s" % (myString, MyDropDownMenu, myOptionalText)
        
        # return (result,)
        # return {"result": (result,)}
        return {"ui": {"text": (r,)}, "result": (r,)}



NODE_CLASS_MAPPINGS = {
    "TestNode": TestNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TestNode": "TestNodeName",
}

