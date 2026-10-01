from pathlib import Path
import re


config = Path(__file__).resolve().parents[1] / "config"
keymap = (config / "klotz.keymap").read_text()
behaviors = (config / "custom-behaviors.dtsi").read_text()
combos = (config / "combos.dtsi").read_text()


def keys(layer):
    body = keymap.split(f"LAYER({layer},", 1)[1].split("\n)\n", 1)[0]
    return re.findall(r"&kp\s+([A-Z]+)", body)


assert keys("Base") == "Q W F P G J L U Y SEMI A R S T D H N E I O Z X C V B K M COMMA DOT SLASH".split()
assert keys("Korean") == "Q W E R T Y U I O SLASH A S D F G H J K L P Z X C V B B N M COMMA DOT".split()
assert "#define KOREAN      1" in keymap
assert "&lang_num NUM 0" in keymap
assert "&mac_lang_num NUM 0" in keymap
assert "&tog KOREAN" in keymap
assert "bindings = <&kp LANG1 &tog KOREAN>;" in behaviors
assert "bindings = <&kp F18 &tog KOREAN>;" in behaviors
assert "combo_lang,  &lang_win" in combos
assert "combo_lang_m, &lang_mac" in combos
print("Colemak/Korean keymap check passed")
