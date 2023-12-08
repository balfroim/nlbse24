# STACK_TRACE_RECORDER_CODE = """package {package};

# import java.io.BufferedWriter;
# import java.io.IOException;
# import java.io.PrintWriter;
# import java.util.regex.Matcher;
# import java.util.regex.Pattern;



# /**
#  * Utility class to record a stack trace from a specified method to the end of
#  * the stack trace.
#  */
# public class StackTraceRecorder {{

#     private String testName;
#     private String fixedMethodName;
#     private String path;
#     private StackTraceElement[] stacktrace;
#     private String encoding = "UTF-8";


#     public StackTraceRecorder(String testName, String fixedMethodName, String path) {{
#         this.testName = testName;
#         this.fixedMethodName = fixedMethodName;
#         this.path = path;
#     }}

#     public void recordStackTrace() {{
#         stacktrace = Thread.currentThread().getStackTrace();

#         if (isMethodInStackTrace(testName) && isMethodInStackTrace(fixedMethodName)) {{
#             writeStackTraceToFile();
#         }}
#     }}

#     /**
#      * Checks if a specified method name is present in the stack trace.
#      *
#      * @param methodName the name of the method to look for
#      * @return true if the method name is found in the stack trace, false otherwise
#      */
#     private boolean isMethodInStackTrace(String methodName) {{
#         for (StackTraceElement element : stacktrace) {{
#             if (methodName.equals(element.getMethodName())) {{
#                 return true;
#             }}
#         }}
#         return false;
#     }}

#     /**
#      * Writes the stack trace to a file starting from the specified method name.
#      */
#     private void writeStackTraceToFile() {{
#         try {{
#             PrintWriter file = new PrintWriter(this.path, encoding);
#             BufferedWriter writer = new BufferedWriter(file);
#             writer.write("package,file,class,method,line number");
#             writer.newLine();
#             boolean startRecording = false;

#             for (int i = stacktrace.length - 1; i >= 0; i--) {{
#                 StackTraceElement element = stacktrace[i];
                
#                 if (testName.equals(element.getMethodName())) {{
#                     startRecording = true;
#                 }}
#                 if (startRecording) {{
#                     String pattern = "(.*)\\\\.(.*)";
#                     Pattern r = Pattern.compile(pattern);
#                     Matcher m = r.matcher(element.getClassName());
#                     if (!m.find()) {{
#                         continue;
#                     }} 
#                     String packageName = m.group(1);
#                     String className = m.group(2);
#                     int lineNumber = element.getLineNumber();
#                     writer.write(String.format("%s,%s,%s,%s,%d", packageName, element.getFileName(), className, element.getMethodName(), lineNumber));
#                     writer.newLine();
#                 }}
#                 if (fixedMethodName.equals(element.getMethodName())) {{
#                     break;
#                 }}
#             }}
#             writer.flush();
#             writer.close();
#         }} catch (IOException e) {{
#             System.err.println("Exception: " + e.getMessage());
#         }}
#     }}
# }}
# """
STACK_TRACE_RECORDER_CODE = """package {package};

import java.io.BufferedWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.regex.Matcher;
import java.util.regex.Pattern;



/**
 * Utility class to record a stack trace from a specified method to the end of
 * the stack trace.
 */
public class StackTraceRecorder {{

    private String testName;
    private String fixedMethodName;
    private String path;
    private StackTraceElement[] stacktrace;
    private String encoding = "UTF-8";


    public StackTraceRecorder(String testName, String fixedMethodName, String path) {{
        this.testName = testName;
        this.fixedMethodName = fixedMethodName;
        this.path = path;
    }}

    public void recordStackTrace() {{
        stacktrace = Thread.currentThread().getStackTrace();

        if (isMethodInStackTrace(testName) && isMethodInStackTrace(fixedMethodName)) {{
            writeStackTraceToFile();
        }}
    }}

    /**
     * Checks if a specified method name is present in the stack trace.
     *
     * @param methodName the name of the method to look for
     * @return true if the method name is found in the stack trace, false otherwise
     */
    private boolean isMethodInStackTrace(String methodName) {{
        for (int i = 0; i < stacktrace.length; i++) {{
            StackTraceElement element = stacktrace[i];
            if (methodName.equals(element.getMethodName())) {{
                return true;
            }}
        }}
    
        return false;
    }}

    /**
     * Writes the stack trace to a file starting from the specified method name.
     */
    private void writeStackTraceToFile() {{
        try {{
            PrintWriter file = new PrintWriter(this.path, encoding);
            BufferedWriter writer = new BufferedWriter(file);
            writer.write("package,file,class,method,line number");
            writer.newLine();
            boolean startRecording = false;

            for (int i = stacktrace.length - 1; i >= 0; i--) {{
                StackTraceElement element = stacktrace[i];
                
                if (testName.equals(element.getMethodName())) {{
                    startRecording = true;
                }}
                if (startRecording) {{
                    String pattern = "(.*)\\\\.(.*)";
                    Pattern r = Pattern.compile(pattern);
                    Matcher m = r.matcher(element.getClassName());
                    if (!m.find()) {{
                        continue;
                    }} 
                    String packageName = m.group(1);
                    String className = m.group(2);
                    int lineNumber = element.getLineNumber();
                    StringBuffer buffer = new StringBuffer();
                    buffer.append(packageName);
                    buffer.append(',');
                    buffer.append(element.getFileName());
                    buffer.append(',');
                    buffer.append(className);
                    buffer.append(',');
                    buffer.append(element.getMethodName());
                    buffer.append(',');
                    buffer.append(lineNumber);

                    writer.write(buffer.toString());
                    writer.newLine();
                }}
                if (fixedMethodName.equals(element.getMethodName())) {{
                    break;
                }}
            }}
            writer.flush();
            writer.close();
        }} catch (IOException e) {{
            System.err.println("Exception: " + e.getMessage());
        }}
    }}
}}
"""

STACK_TRACE_RECORDER_LINE = "StackTraceRecorder recorder = new StackTraceRecorder(\"{test_name}\", \"{method_name}\", \"./{stacktrace_csv}\");\nrecorder.recordStackTrace();\n"

FIXED_BUILD_CHART = """<!-- An ANT build file for JFreeChart -->

<!-- Written by David Gilbert. -->
<!-- 2-Jan-2003 -->

<!-- Tested with Ant 1.6.5 -->
<!-- To run this script, you need to make sure the libraries used by -->
<!-- JFreeChart are copied to the ../lib directory (or edit the -->
<!-- initialise task to point to the appropriate jar files). -->

<!-- If you have comments about this script, please post a message -->
<!-- on the JFreeChart developers mailing list. -->

<project name="jfreechart" default="all" basedir="..">

    <!-- Initialisation. -->
    <target name="initialise" description="Initialise required settings.">
        <tstamp />
        <property name="jfreechart.name" value="jfreechart" />
        <property name="jfreechart.version" value="1.2.0-pre1" />
        <property name="jfreechart-bundle-file" value="${jfreechart.name}-${jfreechart.version}-bundle.jar" />
        <property name="itext.name" value="itext" />
        <property name="itext.version" value="2.0.2" />
        <property name="itext.jar" value="${basedir}/lib/${itext.name}-${itext.version}.jar"/>
        <property name="builddir" value="${basedir}/build" />
        <property name="servlet.jar" value="${basedir}/lib/servlet.jar"/>
        <property name="junit.jar" value="${basedir}/lib/junit.jar"/>
        <available classname="javax.imageio.ImageIO" property="ImageIO.present"/>
        <path id="build.classpath">
            <pathelement location="${servlet.jar}"/>
        </path>

    </target>

    <!-- Compile the JFreeChart classes -->
    <target name="compile" depends="initialise"
            description="Compile the JFreeChart source code.">

        <!-- create a temp build directory -->
        <mkdir dir="${basedir}/build" />

        <!-- compile the source -->
        <javac srcdir="${basedir}/source" 
               destdir="${basedir}/build"
               debug="on"
               deprecation="false"
               source="1.4"
               target="1.4">
            <classpath refid="build.classpath" />
            <include name="org/jfree/**"/>       	
        </javac>

        <!-- copy across gorilla.jpg -->
        <copy file="${basedir}/source/org/jfree/chart/gorilla.jpg" tofile="${basedir}/build/org/jfree/chart/gorilla.jpg" />

        <!-- copy across .properties files -->
        <copy todir="${basedir}/build/org/jfree/chart/">
            <fileset dir="${basedir}/source/org/jfree/chart">
                <include name="*.properties" />
            </fileset>
        </copy>
        <copy todir="${basedir}/build/org/jfree/chart/plot">
            <fileset dir="${basedir}/source/org/jfree/chart/plot">
                <include name="*.properties" />
            </fileset>
        </copy>
        <copy todir="${basedir}/build/org/jfree/chart/editor">
            <fileset dir="${basedir}/source/org/jfree/chart/editor">
                <include name="*.properties" />
            </fileset>
        </copy>
        <copy todir="${basedir}/build/org/jfree/chart/ui">
            <fileset dir="${basedir}/source/org/jfree/chart/ui">
                <include name="*.properties" />
            </fileset>
        </copy>

        <!-- make the jar -->
        <jar jarfile="${basedir}/${jfreechart.name}-${jfreechart.version}.jar"
             basedir="${basedir}/build" >
        </jar>

        <!-- delete the temp directory -->
        <delete dir="${basedir}/build" />

    </target>


    <!-- Compile the experimental classes --> 
    <target name="compile-experimental" depends="compile" 
            description="Compile the JFreeChart experimental classes"> 

        <!-- create a temp build directory -->
        <mkdir dir="${basedir}/build" />

        <path id="build.experimental.classpath">
            <pathelement location="${servlet.jar}"/>
            <pathelement location="${basedir}/${jfreechart.name}-${jfreechart.version}.jar"/>
        </path>

        <!-- compile the source -->
        <javac srcdir="${basedir}/experimental" 
               destdir="${basedir}/build"
               debug="on"
               deprecation="false"
               source="1.4"
               target="1.4">
            <classpath refid="build.experimental.classpath" />
            <include name="org/jfree/experimental/**"/>
            <exclude name="org/jfree/experimental/**/junit/*"/>
        </javac>

        <!-- make the jar -->
        <jar jarfile="${basedir}/${jfreechart.name}-${jfreechart.version}-experimental.jar"
             basedir="${basedir}/build" >
        </jar>

        <!-- delete the temp directory -->
        <delete dir="${basedir}/build" />
    </target>
	
	
    <!-- Fill the 'distribution' directory. -->
    <target name="fill-distribution" depends="compile">
	
        <!-- delete the temporary distribution directory, if there is one -->
        <delete dir="${basedir}/distribution" />

    	<!-- make a temporary distribution directory -->
        <mkdir dir="${basedir}/distribution" />

        <!-- copy across README and CHANGELOG -->
        <copy file="${basedir}/README.txt" tofile="${basedir}/distribution/README.txt" />
        <copy file="${basedir}/NEWS" tofile="${basedir}/distribution/NEWS" />
        <copy file="${basedir}/ChangeLog" tofile="${basedir}/distribution/ChangeLog" />
        <copy file="${basedir}/maven-jfreechart-project.xml" tofile="${basedir}/distribution/maven-jfreechart-project.xml" />

        <!-- copy across LICENCE -->
        <copy file="${basedir}/licence-LGPL.txt" tofile="${basedir}/distribution/licence-LGPL.txt" />

        <!-- copy across runtime jar file and demo jar file -->
        <copy file="${basedir}/${jfreechart.name}-${jfreechart.version}.jar" tofile="${basedir}/distribution/lib/${jfreechart.name}-${jfreechart.version}.jar" />
        <copy file="${basedir}/${jfreechart.name}-${jfreechart.version}-experimental.jar" tofile="${basedir}/distribution/lib/${jfreechart.name}-${jfreechart.version}-experimental.jar" />
        <copy file="${basedir}/${jfreechart.name}-${jfreechart.version}-demo.jar" tofile="${basedir}/distribution/${jfreechart.name}-${jfreechart.version}-demo.jar" failonerror="false" />
    
        <!-- copy across source files -->
        <copy todir="${basedir}/distribution/source">
            <fileset dir="${basedir}/source">
              <exclude name="**/CVS/*"/>
            </fileset>
        </copy>

        <copy todir="${basedir}/distribution/experimental">
            <fileset dir="${basedir}/experimental">
              <exclude name="**/CVS/*"/>
            </fileset>
        </copy>

        <copy todir="${basedir}/distribution/tests">
            <fileset dir="${basedir}/tests">
              <exclude name="**/CVS/*"/>
            </fileset>
        </copy>
    	
        <copy todir="${basedir}/distribution/swt">
            <fileset dir="${basedir}/swt">
              <exclude name="**/CVS/*"/>
            </fileset>
        </copy>    	

        <!-- copy across lib files -->
        <copy file="${basedir}/lib/swtgraphics2d.jar" tofile="${basedir}/distribution/lib/swtgraphics2d.jar" />
        <copy file="${basedir}/lib/jfreechart-${jfreechart.version}-swt.jar" tofile="${basedir}/distribution/lib/${jfreechart.name}-${jfreechart.version}-swt.jar" />
        <copy file="${servlet.jar}" tofile="${basedir}/distribution/lib/servlet.jar" />
        <copy file="${junit.jar}" tofile="${basedir}/distribution/lib/junit.jar" />
        <copy file="${itext.jar}" tofile="${basedir}/distribution/lib/${itext.name}-${itext.version}.jar" />

        <!-- copy across ant build files -->
        <copy file="${basedir}/ant/build.xml" tofile="${basedir}/distribution/ant/build.xml" />
        <copy file="${basedir}/ant/build-swt.xml" tofile="${basedir}/distribution/ant/build-swt.xml" />

        <!-- copy across checkstyle property file -->
        <copy todir="${basedir}/distribution/checkstyle">
            <fileset dir="${basedir}/checkstyle" />
        </copy>

        <!-- convert end-of-line characters in text files -->
        <fixcrlf srcdir="${basedir}/distribution/source"
                 eol="crlf" eof="remove"
                 excludes="**/*.jpg" />

        <fixcrlf srcdir="${basedir}/distribution/experimental"
                 eol="lf" eof="remove"
                 excludes="**/*.jpg" />

    	<fixcrlf srcdir="${basedir}/distribution/swt"
                 eol="lf" eof="remove"
                 excludes="**/*.jpg" />

    	<fixcrlf srcdir="${basedir}/distribution/tests"
                 eol="lf" eof="remove"
                 excludes="**/*.jpg" />

    </target>

    <!-- Make .zip distribution for JFreeChart -->
    <target name="zip" depends="fill-distribution">

        <!-- make the zip file -->
        <zip zipfile="${basedir}/${jfreechart.name}-${jfreechart.version}.zip">
             <zipfileset dir="${basedir}/distribution"
                         prefix="${jfreechart.name}-${jfreechart.version}" />
        </zip>

    </target>

    <!-- Make .tar.gz distribution for JFreeChart -->
    <target name="targz" depends="fill-distribution">

        <!-- make the tar.gz file -->
        <tar tarfile="${basedir}/${jfreechart.name}-${jfreechart.version}.tar">
             <tarfileset dir="${basedir}/distribution"
                         prefix="${jfreechart.name}-${jfreechart.version}" />
        </tar>
        <gzip zipfile="${basedir}/${jfreechart.name}-${jfreechart.version}.tar.gz"   
              src="${basedir}/${jfreechart.name}-${jfreechart.version}.tar" />
        <delete file="${basedir}/${jfreechart.name}-${jfreechart.version}.tar" />

    </target>

  <target name="maven-bundle" depends="zip" >
    <!-- make a temporary distribution directory -->
    <mkdir dir="distribution"/>
    <!-- copy across LICENCE -->
    <copy file="licence-LGPL.txt" tofile="distribution/LICENSE.txt"/>
    
    <filterchain id="version.filters">
       <replacetokens>
         <token key="VERSION" value="${jfreechart.version}"/>
       </replacetokens>
    </filterchain>
    <copy file="maven-jfreechart-project.xml" tofile="distribution/project.xml">
	<filterchain refid="version.filters"/>
    </copy>
    
    <!-- copy across runtime jar file -->
    <copy file="${jfreechart.name}-${jfreechart.version}.jar" tofile="distribution/${jfreechart.name}-${jfreechart.version}.jar"/>

    <!-- make the jar -->
    <jar jarfile="${jfreechart-bundle-file}" basedir="distribution"/>

    <!-- delete the temporary distribution directory -->
    <delete dir="distribution"/>
  </target>


    <!-- COMPILE THE JUNIT TESTS. -->  
    <target name="compile-tests" 
            depends="compile,compile-experimental"
            description="Compile the test code">
        
        <mkdir dir="${basedir}/build-tests"/>
        <javac srcdir="${basedir}/tests" 
               destdir="${basedir}/build-tests" 
               source="1.4"
               target="1.4" 
               debug="true" 
               deprecation="false"
               optimize="false">
            <classpath>
                <path refid="build.classpath"/>
                <pathelement location="${junit.jar}"/>
                <pathelement location="${basedir}/${jfreechart.name}-${jfreechart.version}.jar"/>
                <pathelement location="${basedir}/${jfreechart.name}-${jfreechart.version}-experimental.jar"/>
                <pathelement location="${basedir}/build-tests"/>
            </classpath>
        </javac>
    
    </target>


    <!-- RUN THE JUNIT TESTS. -->
    <target name="test" 
            depends="compile-tests"
            description="Run the test cases">
        
        <mkdir dir="${basedir}/build-tests-reports"/>
        
        <junit printSummary="yes" 
               haltonerror="true" 
               haltonfailure="true"
               fork="true" 
               dir=".">
            
            <sysproperty key="basedir" value="."/>
            <formatter type="plain" usefile="false"/>
            <classpath>
                <path refid="build.classpath"/>
                <pathelement location="${junit.jar}"/>
                <pathelement location="${basedir}/${jfreechart.name}-${jfreechart.version}.jar"/>
                <pathelement location="${basedir}/${jfreechart.name}-${jfreechart.version}-experimental.jar"/>
                <pathelement location="${basedir}/build-tests"/>
            </classpath>
            <batchtest todir="${basedir}/build-tests-reports">
                <fileset dir="${basedir}/tests">
                    <include name="**/*Tests.java"/>
                </fileset>
            </batchtest>
        </junit>
    </target>

    <!-- ALL -->
    <target name="all" 
            depends="compile"
            description="Compiles JFreeChart, builds the jar files and creates distribution files (.zip and .tar.gz).">

        <!-- delete the temporary distribution directory -->
        <delete dir="${basedir}/distribution" />    
    </target>

</project>
"""

EXTRACT_METHODS_QLL = """/**
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
        "\\"method_name\\": \\"" + this.getName() + "\\", " +
        "\\"javadoc_start_line\\": " + this.getJavadocStartLine().toString() + ", " +
        "\\"annotations_start_line\\": " + this.getAnnotationsStartLine().toString() + ", " +
        "\\"method_start_line\\": " + this.getMethodStartLine().toString() + ", " +
        "\\"end_line\\": " + this.getEndLine().toString() + 
      "}"
    )
  }

  int getEndLine() { result = this.getBody().getLocation().getEndLine() }
}

 

predicate getMethodOrConstructor(MethodOrConstructor moc, string fileName, int callLine) {
  callLine in [moc.getMethodStartLine()..moc.getEndLine()] and
  moc.getFileName() = fileName
}
"""