import { MarkdownText } from "@/components/markdown/markdownText";

const markdown = `A paragraph with *emphasis* and **strong importance**.

> A block quote with ~strikethrough~ and a URL: https://reactjs.org.

[An inline link](https://www.google.com)

# A header (H1)

## A subheader (H2)

### A subsubheader (H3)

Lists
* [ ] todo
* [x] done

A table:

| head1 | head2 |
| - | - |
| mark1 | mark2 |

The lift coefficient ($C_L$) is a dimensionless coefficient.
~~~python
print("Hello, World!")
~~~
---
`

export default function BlogPage() {
  return (
    <div>
      <MarkdownText text={markdown} />
    </div>
  );

}
