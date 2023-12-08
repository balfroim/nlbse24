SYSTEM_PROMPT_TEMPLATE = """You are a helpful, respectful and honest assistant. Always answer as helpfully
as possible, while being safe. Your answers should not include any harmful,
unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that
your responses are socially unbiased and positive in nature.
If a question does not make any sense, or is not factually coherent, explain why
instead of answering something not correct. If you don’t know the answer to a
question, please don’t share false information.
Your goal is to assist a new programmer in onboarding a software project.
The test has failed with the following error: {error}, and it has produced the following message: {error_message}."""

EXPLAIN_PROMPT_TEMPLATE = """```java
{code_snippet}
```
(Summarize and explain this code snippet in plain English:)"""

EXPLAIN_PROMPT_TEMPLATE_FEWSHOT = """```java
public class PaintWindow {{
    private PaintObject paintObject;

    public PaintWindow() {{
        // Constructor initializes a default PaintObject for pencil drawing
        paintObject = new PaintObject(Color.GREEN, 5); // Green color, thickness 5
    }}

    public void onMouseEvent(MouseEvent e) {{
        // Method to handle mouse events like click, move, and release
        // Delegates the event handling to the PaintObject instance
        paintObject.handleEvent(e);
    }}
}}

public class PaintObject {{
    private Color color;
    private int thickness;

    public PaintObject(Color color, int thickness) {{
        // Constructor to initialize the PaintObject with specified color and thickness
        this.color = color;
        this.thickness = thickness;
    }}

    public void handleEvent(MouseEvent e) {{
        // Logic to handle mouse events and perform drawing on the canvas
        // Details are abstracted for this example
    }}
}}
```
(Summarize and explain this code snippet in plain English:)
\"\"\"
The PaintWindow contains an instance of a PaintObject. This class is responsible for responding to the mouse click, move, and release events the user performs on the application canvas.
In the lines of code above, the object constructor is initialised. By default, the object constructor is set to construct pencil objects on the canvas (i.e. free form strokes) in the color green, thickness 5. The last two lines above set the object constructor as a subscriber to any mouse or mouse motion events that take place on the canvas.
\"\"\"
```java
{code_snippet}
```
(Summarize and explain this code snippet in plain English:)"""

MAX_OUTPUT_TOKENS = 256