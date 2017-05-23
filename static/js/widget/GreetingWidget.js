/**
 * Created by newmember on 17/05/2017.
 */

define([
	"dojo",
	"dojo/_base/declare",
	"dojo/_base/fx",
	"dojo/_base/lang",
	"dojo/dom-style",
	"dojo/mouse",
	'dojo/request/xhr',
	"dojo/dom",
	"dojo/on",
	"dojo/request",
	"dojo/cookie",
	"dijit/_WidgetBase",
	"dijit/_TemplatedMixin",
	"dojo/text!./templates/GreetingWidget.html"
], function (dojo, declare, baseFx, lang, domStyle, mouse, xhr, dom, on, request, cookie, _WidgetBase, _TemplatedMixin, template) {
	return declare("GreetingWidget", [_WidgetBase, _TemplatedMixin], {
		author: "Anonymous",
		content: "",
		guestbookId: "",
		date: "",
		dateUpdate: "",
		updatedBy: "",
		url: "",
		avatarEdit: require.toUrl("../static/images/edit.png"),
		avatarDelete: require.toUrl("../static/images/delete.png"),
		informationNode: "",
		formEditNode: "",
		editContentNode: "",
		submitNode:"",
		templateString: template,
		baseClass: "greetingWidget",
		mouseAnim: null,
		baseBackgroundColor: "#fff",
		mouseBackgroundColor: "#def",

		postCreate: function () {

			var domNode = this.domNode;

			this.inherited(arguments);

			domStyle.set(domNode, "backgroundColor", this.baseBackgroundColor);
			domStyle.set(this.informationNode, "display", "block");
			domStyle.set(this.formEditNode, "display", "none");
			this._showAndHideEditContent(true);

			this.own(
					on(domNode, mouse.enter, lang.hitch(this, "_changeBackground", this.mouseBackgroundColor)),
					on(domNode, mouse.leave, lang.hitch(this, "_changeBackground", this.baseBackgroundColor)),
					on(this.avatarEditNode, "click", lang.hitch(this, "_clickEdit")),
					on(this.avatarDeleteNode, "click", lang.hitch(this, "_clickDelete")),
					on(this.submitNode, "click", lang.hitch(this, "_clickSubmit"))
			);
		},

		_clickEdit: function () {
			this._showAndHideEditContent(false);
		},

		_clickSubmit: function () {
			var instance = this;
			var content = this.editContentNode.value;
			xhr.put(this.url, {
				data: JSON.stringify({message : content}),
				headers: {
					"X-CSRFToken": cookie("csrf_token")
				}
			}).then(function (data) {
				instance._showAndHideEditContent(true);
				alert("Update successed."+ data)
			}, function () {
				alert("Update failed.")
			});
		},

		_showAndHideEditContent: function (value) {
			if (value){
				domStyle.set(this.informationNode, "display", "block");
				domStyle.set(this.formEditNode, "display", "None");
			}else{
				domStyle.set(this.informationNode, "display", "None");
				domStyle.set(this.formEditNode, "display", "block");
			}
		},

		_clickDelete: function () {
			if (confirm("Are you sure to delete?")) {
				xhr.del(this.url, {
					headers: {
						"X-CSRFToken": cookie("csrf_token")
					}
				}).then(function () {
					alert("Delete successed.")
				}, function () {
					alert("Deleted failed.")
				});
			}
		},

		_changeBackground: function (newColor) {
			if (this.mouseAnim) {
				this.mouseAnim.stop();
			}

			this.mouseAnim = baseFx.animateProperty({
				node: this.domNode,
				properties: {
					backgroundColor: newColor
				},
				onEnd: lang.hitch(this, function () {
					this.mouseAnim = null;
				})
			}).play();
		},

		_setAvatarEditAttr: function (imagePath) {
			if (imagePath != "") {
				this._set("avatarEdit", imagePath);
				this.avatarEditNode.src = imagePath;
			}
		},

		_setAvatarDeleteAttr: function (imagePath) {
			if (imagePath != "") {
				this._set("avatarDelete", imagePath);
				this.avatarDeleteNode.src = imagePath;
			}
		},
	});
});
