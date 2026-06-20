/* eslint func-names: ["error", "never"] */
/* eslint-env jquery */
/* eslint no-underscore-dangle: ["error", { "allow": ["__lc"] }] */
/* eslint-disable consistent-return */

(function ($) {
  $(document).ready(function () {
    let inputFieldNumber = 0;
    let printFieldNumber = 0;
    let formField;
    let printField;
    let formFirstBracket = true;
    let letterContent = "";
    function replaceInBrackets(match, p1, p2) {
      let inputSize = 7;
      if (p2.length > inputSize) {
        const canvasText = '<canvas id="canvas"></canvas>';
        $(".content").append(canvasText);
        const canvas = document.getElementById("canvas");
        const ctx = canvas.getContext("2d");
        const text = ctx.measureText(p2);
        inputSize = text.width;
      }
      formField = "";
      if (formFirstBracket) {
        formField += '<form id="form-letter__form">';
        formField += '<div class="form-letter__body">';
        formFirstBracket = false;
      } else {
        inputFieldNumber += 1;
        formField += `<input id="dynamicFormLetterField${inputFieldNumber}"`;
        formField += `name="dynamicFormLetterField${inputFieldNumber}"`;
        formField += 'class="form-letter__field"';
        formField += `style="width:${inputSize}px"`;
        formField += `placeholder="${p2}" requred>`;
      }
      return formField;
    }

    function contentInputFieldsToPlainText() {
      printFieldNumber += 1;
      const dynamicField = document.getElementById(
        `dynamicFormLetterField${printFieldNumber}`
      );
      printField = dynamicField.value;
      return printField;
    }

    function printForm(e) {
      let areFieldsValidated = true;
      let firstMissingField = "#dynamicFormLetterField";
      $(".form-letter__field").each(function (index) {
        if ($(this).val() === "") {
          areFieldsValidated = false;
          firstMissingField += index + 1;
          $(firstMissingField).focus();
          return false;
        }
      });

      e.preventDefault();
      if (areFieldsValidated) {
        const formLetterForm = $("#form-letter__form");
        printFieldNumber = 0;
        let printContent = formLetterForm
          .html()
          .replace(/(<input)(.*?)(>)/g, contentInputFieldsToPlainText);
        printContent = `<div id="form-letter__printout">${printContent}</div>`;

        $(".form-letter__container").append(printContent);

        printJS({
          printable: "form-letter__printout",
          type: "html",
        });

        $("#form-letter__printout").remove();
      }
    }

    function resizeInputLenght() {
      if (this.value !== "" && this.placeholder.length > this.value.length) {
        this.style.width = `${this.value.length}ch`;
      } else {
        this.style.width = `${this.placeholder.length}ch`;
      }
    }

    function addGlobalEventListeners() {
      const formLetterField = $(".form-letter__field");

      $(".form-letter__button").on("click", printForm);
      formLetterField.on("input propertychange", resizeInputLenght);
    }

    function contentBracketsToInputFields() {
      const rowContent = $(".form-letter__container");

      const replacedContent = rowContent
        .html()
        .replace(/({{2})(.*?)(}{2})/g, replaceInBrackets);

      letterContent += replacedContent;
      letterContent += "</div>";
      letterContent += "</form>";
      letterContent +=
        '<button type="submit" aria-label="Print letter with populated fields"';
      letterContent += 'data-is-template="true" formnovalidate=""';
      letterContent += 'class="form-letter__button">Print template';
      letterContent += "</button>";

      $(".form-letter__container").html(letterContent);
    }

    contentBracketsToInputFields();
    addGlobalEventListeners();
  });
})(jQuery);
