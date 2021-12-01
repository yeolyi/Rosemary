import os
import pathlib
from pathlib import Path
from posixpath import splitext
import frontmatter
import shutil

root_path = Path(__file__).parent.parent


def load_template(path):
    template_full_path = os.path.join(root_path, "template", path)
    f = open(template_full_path, "r")
    ret = f.read()
    f.close()
    return ret


def build_html(path, **kwargs):
    import re

    src = load_template(path)
    startKwIdx = [_.start() for _ in re.finditer("!@", src)]
    endKwIdx = [_.start() for _ in re.finditer("@!", src)]
    startPos = 0
    ret = ""
    for i in range(len(startKwIdx)):
        lo = startKwIdx[i]
        hi = endKwIdx[i]
        ret += src[startPos:lo]
        kw = src[lo + 2 : hi]
        ret += kwargs[kw]
        startPos = hi + 2
    ret += src[startPos:]
    return ret


# 일대일 대응인걸로 하자
def parse_src(template_path, src_path, **kwargs):
    from markdown import markdown
    import frontmatter

    src_full_path = os.path.join(root_path, "src", src_path)
    src = frontmatter.load(src_full_path)
    src["file_name"] = os.path.basename(Path(src_full_path).parent)

    for (key, f) in kwargs.items():
        if key == "others":
            kwargs["others"](src)
        else:
            kwargs[key] = f(src[key])

    kwargs["content"] = markdown(
        src.content,
        extensions=["markdown.extensions.fenced_code", "markdown.extensions.attr_list"],
    )
    return build_html(template_path, **kwargs)


def one_folder_one_post(src_path, dst_path, transform, key=None):
    import shutil

    src_full_path = os.path.join(root_path, "src", src_path)
    dst_full_path = os.path.join(root_path, "public", dst_path)
    src_folder_names = list(filter(lambda x: x[0] != ".", os.listdir(src_full_path)))
    if key != None:
        src_folder_names.sort(key=key, reverse=True)

    for src_folder_name in src_folder_names:
        post_src_path = os.path.join(src_full_path, src_folder_name)
        post_dst_path = os.path.join(dst_full_path, src_folder_name)
        Path(post_dst_path).mkdir(parents=True, exist_ok=False)

        # 특정 글에 속한 모든 파일을 순회

        for post_comp_name in os.listdir(post_src_path):
            post_comp_path = os.path.join(post_src_path, post_comp_name)
            ext_name = os.path.splitext(post_comp_name)[1]
            if post_comp_name == "content.md":
                converted = transform(
                    os.path.join(src_path, src_folder_name, post_comp_name)
                )
                with open(os.path.join(post_dst_path, "index.html"), "w") as f:
                    f.write(converted)
            elif ext_name == ".png" or ext_name == ".jpg" or ext_name == ".jpeg":
                shutil.copy2(post_comp_path, post_dst_path)


def make_writings():
    rows = ""

    def writing_transform(content_path):
        def makeRow(src):
            nonlocal rows
            rows += build_html(
                "writing/row.html",
                title=src["title"],
                date=str(src["date"]),
                link=f"/stories/writing/{src['file_name']}",
            )

        return parse_src(
            "writing/post.html",
            content_path,
            title=lambda x: x,
            date=lambda x: str(x),
            others=makeRow,
        )

    def date_of_story(path):
        p = os.path.join(root_path, "src/writing", path, "content.md")
        with open(p, "r+") as f:
            post = frontmatter.load(f)
            return post["date"]

    shutil.rmtree(os.path.join(root_path, "public/stories/writing"), ignore_errors=True)
    one_folder_one_post("writing", "stories/writing", writing_transform, date_of_story)

    with open(os.path.join(root_path, "public/stories/index.html"), "w") as f:
        f.write(build_html("writing/list.html", rows=rows))


def make_til():
    rows = ""

    def date_of_til(path):
        p = os.path.join(root_path, "src/til", path, "content.md")
        with open(p, "r+") as f:
            post = frontmatter.load(f)
            return str(post["date"])

    def time_table_parser(src):
        ret = ""
        for time_table_title in src:
            ret += build_html(
                "til/time_table.html",
                title=time_table_title,
                time=str(src[time_table_title]),
            )
        return ret

    def til_transform(content_path):
        def makeRow(src):
            nonlocal rows
            rows += build_html(
                "til/row.html", date=str(src["date"]), link=f"{src['file_name']}"
            )

        def date_to_title(date):
            return "\n".join(str(date).split("-"))

        return parse_src(
            "til/post.html",
            content_path,
            date=date_to_title,
            time_table=time_table_parser,
            others=makeRow,
        )

    shutil.rmtree(os.path.join(root_path, "public/stories/til"), ignore_errors=True)
    one_folder_one_post("til", "stories/til", til_transform, date_of_til)

    with open(os.path.join(root_path, "public/stories/til/index.html"), "w") as f:
        f.write(build_html("til/list.html", rows=rows))


def make_archieve():
    rows = ""

    def archieve_transform(content_path):
        def makeRow(src):
            nonlocal rows
            rows += build_html(
                "archieve/row.html", title=src["title"], link=f"{src['file_name']}"
            )

        return parse_src(
            "archieve/post.html",
            content_path,
            title=lambda x: x,
            others=makeRow,
        )

    shutil.rmtree(
        os.path.join(root_path, "public/stories/archieve"), ignore_errors=True
    )
    one_folder_one_post("archieve", "stories/archieve", archieve_transform)

    with open(os.path.join(root_path, "public/stories/archieve/index.html"), "w") as f:
        f.write(build_html("archieve/list.html", rows=rows))


def preserve_hierachy():
    import glob

    for path in glob.iglob(os.path.join(root_path, "src/dict/**/*"), recursive=True):
        new_path = str(Path(path).parent).replace("src", "public")
        Path(new_path).mkdir(parents=True, exist_ok=True)
        ext = os.path.splitext(path)[1]
        if ext == ".md":
            compact_path = os.path.relpath(path, os.path.join(root_path, "public"))
            with open(path, "r") as f:
                converted = parse_src(
                    "archieve/post.html", compact_path, title=lambda x: x
                )
                new_path += "/" + os.path.basename(path)[:-2] + "html"
                with open(new_path, "w") as f2:
                    f2.write(converted)
        elif ext == ".png" or ext == ".jpg" or ext == ".jpeg":
            new_path = str(Path(path).parent).replace("src", "public")
            shutil.copy2(path, new_path)
