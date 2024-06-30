/*
    Inserts a given text into the easyMDE textarea and the current cursor location.
 */

function InsertMDE(textToInsert) {
    const editor = easyMDE.codemirror;
    const pos = editor.getCursor();
    editor.replaceRange(textToInsert, pos);
}
