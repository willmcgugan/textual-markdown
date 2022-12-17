# Textual Markdown Browser

This project is an experiment to see how far I could take the idea of a "Markdown browser" in the terminal, using the [Textual](https://github.com/Textualize/textual) framework.

Markdown in the terminal is not unusual, [Rich](https://github.com/Textualize/rich) has a decent Markdown renderer, but its output is essentially static. Textual Markdown creates a more dynamic Markdown document you can interact with: there are working links, srollablr code fences, and tables.

Links must be relative only and on the filesystem for now. These could be made to load from the network for a more browser like experience. It is also relatively easy to intercept links and handle them programatically. Opening up custom hypertext like applications.

And finally, there is a TOC (Table Of Contents) extracted from the Markdown, which can be used to navigate the document.

## Video

A short video of me playing with the demo Markdown.

https://user-images.githubusercontent.com/554369/208234316-be4e6626-c601-4dca-b8d1-59af9b4d08cd.mov


## Screenshots

![Screenshot 2022-12-17 at 08 41 58](https://user-images.githubusercontent.com/554369/208233944-542b1fec-daaf-4c4b-81d1-2d9eec61e727.png)


![Screenshot 2022-12-17 at 08 42 33](https://user-images.githubusercontent.com/554369/208233987-9667dd87-5ef3-45c3-91fc-166f069e14cb.png)

![Screenshot 2022-12-17 at 08 42 38](https://user-images.githubusercontent.com/554369/208233988-f0733761-6794-41f9-893f-f0258b23b988.png)

## Try it out

You can install `textual-markdown` from PyPI in the usual way:

```
pip install textual-markdown
```

Here's how you hopen a Markdown file:

```
python -m textual_markdown README.md
```

## Disclaimer

At time of writing, there is less than a weeks work in this. Which means you may (likely) find bugs. 

## The future

Some (or all) of this repo will be rolled in to [Textual](https://github.com/Textualize/textual). It may also become a project in its own right. If there is enough interest.
