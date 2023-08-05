# Wagtail UI Plus

This Wagtail app provides several ui improvements to the Wagtail admin.

**Conditional checkboxes**
- Automatically check a target checkbox whenever a trigger checkbox is checked
- The reverse also applies, when the target checkbox is unchecked, the trigger checkbox is also unchecked
- This functionality can be used to create an "all" option among a list of checkboxes
- Supported trigger elements: `BooleanField`
- Supported target elements: `BooleanField`

**Conditional visibility**
- Show or hide form fields based on conditional visibility rules
- Regular page fields:
  - Supported trigger elements: `CharField` (with choices), `BooleanField`
  - Supported target elements: Any subclass of `EditHandler`
- Struct block fields:
  - Supported trigger elements: `ChoiceBlock`
  - Supported target elements: Any subclass of `FieldBlock` (within the same struct block)

**Collapsable panels**
- Click on the panel header to collapse/expand the panel
- Set the default collapsed state
- Supported panels: `MultiFieldPanel` and `StreamFieldPanel`

**Stream field improvements**
- Added borders around blocks
- Added panel-style headers to blocks
- Added spacing between blocks
- Permanently visible add buttons
- Use more of the available space for blocks
- Supported blocks: `CharBlock`, `TextBlock`, `EmailBlock`, `IntegerBlock`, `FloatBlock`, `DecimalBlock`, `RegexBlock`, `URLBlock`, `BooleanBlock`, `DateBlock`, `TimeBlock`, `DateTimeBlock`, `RichTextBlock`, `RawHTMLBlock`, `BlockQuoteBlock`, `ChoiceBlock`, `PageChooserBlock`, `DocumentChooserBlock`, `ImageChooserBlock`, `SnippetChooserBlock`, `EmbedBlock`, `StaticBlock`, `StructBlock` and `StreamBlock`

**Struct block improvements**
- All of the above stream field improvements
- If the first field in the struct block is a `CharBlock`, `TextBlock` or `RichtTextBlock`, show it's value in the block header after the block type
- Click on the block header to collapse/expand the struct block
- All struct blocks are default collapsed on page load, but newly added blocks are default expanded

## Compatibility
- Wagtail 2.6.2

## Installation

- `pip install wagtailuiplus`
- Add `wagtailuiplus` to your installed apps

## Usage

**Conditional checkboxes**
- Add the class `wagtailuiplus__checkbox-handler` to the trigger element
- Add the class `wagtailuiplus__checkbox-handler--{block_name}` to the trigger element, where `{block_name}` is equal to the block name of the trigger element
- Add the class `wagtailuiplus__checkbox-handler-target--{block_name}` to each target element, where `{block_name}` is equal to the block name of the trigger element
- Add conditional visibility rules to the target elements

To check a target checkbox when the trigger field is checked:
- Add the class `wagtailuiplus__checkbox-handler-checked-if--checked` to the target element

![Screenshot](https://raw.githubusercontent.com/davidcondenl/wagtailuiplus/master/examples/conditional-checkboxes.gif)

**Conditional visibility**

Steps to configure conditional visibility rules:
- Add the class `wagtailuiplus__choice-handler` to the trigger element
- Add the class `wagtailuiplus__choice-handler--{block_name}` to the trigger element, where `{block_name}` is equal to the block name of the trigger element
- Add the class `wagtailuiplus__choice-handler-target--{block_name}` to each target element, where `{block_name}` is equal to the block name of the trigger element
- Add conditional visibility rules to the target elements

To hide a target element if the trigger field has a certain value:
- Add the class `wagtailuiplus__choice-handler-hidden-if--{value}` to the target element, where `{value}` is the value of the trigger element


To match the values of a `BooleanField`, use the string value `true` or `false`. Multiple rules on the same target element are treated as an `or`, so if any of the rules match, the element is hidden. In the following example, conditional visibility is used to show a page chooser when building an internal link, or show a text input when building an external link:

```
class LinkBlock(StructBlock):
    link_type = ChoiceBlock(
        choices = [
            ('internal', 'Internal link'),
            ('external', 'External link'),
        ],
        required=True,
        default='internal',
        label='Link type',
        classname=(
            'wagtailuiplus__choice-handler '
            'wagtailuiplus__choice-handler--link_type'
        )
    )
    link_page = PageChooserBlock(
        required=False,
        label='Link page',
        classname=(
            'wagtailuiplus__choice-handler-target--link_type '
            'wagtailuiplus__choice-handler-hidden-if--external'
        ),
    )
    link_url = CharBlock(
        required=False,
        label='Link url',
        classname=(
            'wagtailuiplus__choice-handler-target--link_type '
            'wagtailuiplus__choice-handler-hidden-if--internal'
        ),
    )
```

![Screenshot](https://raw.githubusercontent.com/davidcondenl/wagtailuiplus/master/examples/conditional-visibility.gif)

**Collapsable panels**

The panels automatically become collapsable. To set the initial collapsed state of panels, add the `wagtailuiplus__panel--collapsed` classname to the panel, for example:

```
class HomePage(Page):
    content_panels = [
        MultiFieldPanel([
            FieldPanel('title'),
        ], 'My multi field panel', classname='wagtailuiplus__panel--collapsed'),
    ]
```

![Screenshot](https://raw.githubusercontent.com/davidcondenl/wagtailuiplus/master/examples/collapsable-panels.png)

**StreamField UI improvements**

The UI improvements automatically apply. Just create your StreamField as usual, for example:

```
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.core.blocks import (
  CharBlock,
  StreamBlock,
  StructBlock,
  RichTextBlock,
)
from wagtail.core.fields import StreamField
from wagtail.core.models import Page


class MyCharBlock(CharBlock):
    class Meta:
        icon = 'pilcrow'
        label = 'My char block'


class MyRichTextBlock(RichTextBlock):
    class Meta:
        icon = 'openquote'
        label = 'My rich text block'


class MyStreamBlock(StreamBlock):
    title = MyCharBlock()
    text = MyRichTextBlock()

    class Meta:
        label = 'My stream block'


class MyStructBlock(StructBlock):
    items = MyStreamBlock(required=False)

    class Meta:
        icon = 'list-ul'
        label = 'My struct block'


class HomePage(Page):
    my_stream_field = StreamField([
            ('my_title_block', MyCharBlock()),
            ('my_text_block', MyRichTextBlock()),
            ('my_struct_block', MyStructBlock()),
        ], blank=True, verbose_name='My stream field')

    content_panels = [
        StreamFieldPanel('my_stream_field'),
    ]
```
![Screenshot](https://raw.githubusercontent.com/davidcondenl/wagtailuiplus/master/examples/streamfield-improvements.png)
