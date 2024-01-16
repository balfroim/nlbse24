EXTRACT_METHODS_QUERY = """/**
* @name Extract methods
* @description Extracts the start and end lines of methods or constructors from a Java class or interface.
* @id java/extract-methods
* @kind problem
* @problem.severity warning
*/
import java
import method_extract

from MethodOrConstructor moc
where 
(
\t{joined_expressions}
)
select moc, moc.toJson()
"""

EXTRACT_METHODS_ORDERED_QUERY = """/**
 * @name Extract methods ordered
 * @description Extracts the start and end lines of methods or constructors from a Java class or interface in order.
 * @id java/extract-methods-ordered
 * @kind problem
 * @problem.severity warning
 */
import java
import method_extract

from MethodOrConstructor moc, int call_order
where 
(
{joined_expressions}
)
select moc, call_order.toString() + "|" + moc.toJson()
"""
