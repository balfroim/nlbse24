/**
* @name Extract method boundaries
* @description Extracts the start and end lines of methods or constructors from a Java class or interface.
* @id java/extract-method-boundaries
* @kind problem
* @problem.severity warning
*/
import java

 

class MethodOrConstructor extends Callable {
  MethodOrConstructor() { this instanceof Method or this instanceof Constructor}

 

  string getFileName() { result = this.getLocation().getFile().getBaseName() }

 

  int getAnnotationsStartLine() {
    if exists(this.getAnAnnotation()) then
      result = min(int line | line = this.getAnAnnotation().getLocation().getStartLine())
    else
      result = this.getLocation().getStartLine()
  }

 

  int getJavadocStartLine() {
    if exists(this.getDoc().getJavadoc()) then
      result = this.getDoc().getJavadoc().getLocation().getStartLine()
    else
      result = this.getLocation().getStartLine()
  }

  int getMethodStartLine() {
    result = this.getBody().getLocation().getStartLine()
  }

  string toJson() {
    result = (
      "{" + 
        "\"method_name\": \"" + this.getName() + "\", " +
        "\"javadoc_start_line\": " + this.getJavadocStartLine().toString() + ", " +
        "\"annotations_start_line\": " + this.getAnnotationsStartLine().toString() + ", " +
        "\"method_start_line\": " + this.getMethodStartLine().toString() + ", " +
        "\"end_line\": " + this.getEndLine().toString() + 
      "}"
    )
  }

  int getEndLine() { result = this.getBody().getLocation().getEndLine() }
}

 

predicate getMethodOrConstructor(MethodOrConstructor moc, string fileName, int callLine) {
  callLine in [moc.getMethodStartLine()..moc.getEndLine()] and
  moc.getFileName() = fileName
}
