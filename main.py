import math
import sys
from pathlib import Path
from wand.image import Image
from wand.color import Color
from wand.drawing import Drawing
from yaml import load, Loader
from default import default_config


def patch_config(patch: dict, config: dict):
    config = config.copy()
    for key, value in patch.items():
        if config.get(key) is not None:
            patch_value_is_dict = isinstance(patch[key], dict)
            config_value_is_dict = isinstance(config[key], dict)

            if patch_value_is_dict and config_value_is_dict:
                config[key] = patch_config(patch[key], config[key])
                continue

        config[key] = patch[key]
    return config


def load_config(config_path: Path):
    if config_path.is_file() and config_path.suffix == 'yaml':
        file = config_path.open(mode='r')
        config = load(stream=file, Loader=Loader)
    else:
        cofig = {}
    effective_config = patch_config(config, default_config)
    print("LOADED CONFIG")
    print(config)
    print("EFFECTIVE CONFIG")
    print(effective_config)
    return effective_config


def scale_image(target_width: int, target: Image):
    result = target.clone()

    scale_factor = target_width / target.width
    width = math.ceil(target.width * scale_factor)
    height = math.ceil(target.height * scale_factor)

    result.resize(width=width, height=height)

    return result


def draw_to_image_canvas(image: Image, canvas: Image, top: int, left: int):
    output_canvas = canvas.clone()
    with Drawing() as draw:
        draw.composite(
            image=image,
            left=left,
            top=top,
            width=image.width,
            height=image.height,
            operator='over'
        )
        draw(output_canvas)
    return output_canvas


def build_output(target: Image, styles: dict):
    canvas = Image(
        width=styles['frame']['width'],
        height=styles['frame']['height'],
        background=Color(styles['frame']['background'])
    )
    scaled = scale_image(
        target_width=styles['image']['width'],
        target=target
    )
    return draw_to_image_canvas(
        image=scaled,
        canvas=canvas,
        top=styles['image']['top'],
        left=styles['image']['left']
    )


def main():
    if len(sys.argv) > 2:
        config_path = Path(sys.argv[1])
    else:
        config_path = Path('config.yaml')

    config = load_config(config_path)

    input_path = Path(config['input'])
    output_path = Path(config['output'])

    if input_path.is_dir():
        if not output_path.is_dir():
            output_path.mkdir(parents=True)
        for path in input_path.iterdir():
            if path.is_file():
                image = Image(filename=path)
                filename = output_path.joinpath(path.name)
                build_output(
                    target=image,
                    styles=config["styles"]
                ).save(
                    filename=filename
                )

    if input_path.is_file():
        image = Image(filename=input_path)
        if not output_path.parent.is_dir():
            output_path.parent.mkdir(parents=True)
        build_output(
            target=image,
            styles=config["styles"]
        ).save(
            filename=output_path
        )


if __name__ == '__main__':
    main()
