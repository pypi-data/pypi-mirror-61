# NLP JP Gears

![](https://github.com/tokusumi/nlp-jp-gears/workflows/Tests/badge.svg)

## Overview

日本語の自然言語処理で頻出の前処理をまとめたものです。pipelineをしいて、複数の処理をまとめることができます。

## API

- pipelineの作成: composer.Composer
- 全角英数字記号を半角に変換: zenhan.ZenToHanConverter
- 半角英数字記号を全角に変換: zenhan.HanToZenConverter
- 括弧とその間のテキストを削除: remover.TextBtwBracketsRemover

## Example

```py
>>> from nlp_jp_gears import Composer
>>> from nlp_jp_gears import (
...     ZenToHanConverter,
...     TextBtwBracketsRemover
... )
>>>
>>> txt_btw_brackets_remover = TextBtwBracketsRemover()
>>> print(txt_btw_brackets_remover.removes)
<{[(「『（［〈《〔｛«‹
>>>
>>> zenhan_converter = ZenToHanConverter()
>>> print(zenhan_converter.converts)
！＂＃＄％＆＇（）＊＋，－．／：；＜＝＞？＠［＼］＾＿｀｛｜｝～０１２３４５６７８９ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ
>>>
>>> composer = Composer(txt_btw_brackets_remover, zenhan_converter)
>>> text = "Ｐｙｔｈｏｎ（パイソン）で自然言語処理？"
>>> out = composer(text)
>>> print(out)
Pythonで自然言語処理?
```
