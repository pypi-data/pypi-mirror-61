(self.webpackJsonp=self.webpackJsonp||[]).push([[105],{176:function(e,t,r){"use strict";var i=r(8);t.a=Object(i.a)(e=>(class extends e{static get properties(){return{hass:Object,localize:{type:Function,computed:"__computeLocalize(hass.localize)"}}}__computeLocalize(e){return e}}))},178:function(e,t,r){"use strict";r.d(t,"a",function(){return a});r(108);const i=customElements.get("iron-icon");let s=!1;class a extends i{constructor(...e){var t,r,i;super(...e),i=void 0,(r="_iconsetName")in(t=this)?Object.defineProperty(t,r,{value:i,enumerable:!0,configurable:!0,writable:!0}):t[r]=i}listen(e,t,i){super.listen(e,t,i),s||"mdi"!==this._iconsetName||(s=!0,r.e(84).then(r.bind(null,236)))}}customElements.define("ha-icon",a)},182:function(e,t,r){"use strict";r.d(t,"a",function(){return a});var i=r(8),s=r(14);const a=Object(i.a)(e=>(class extends e{fire(e,t,r){return r=r||{},Object(s.a)(r.node||this,e,t,r)}}))},197:function(e,t,r){"use strict";r.d(t,"a",function(){return a}),r.d(t,"b",function(){return n}),r.d(t,"c",function(){return o});var i=r(14);const s=()=>Promise.all([r.e(0),r.e(1),r.e(128),r.e(33)]).then(r.bind(null,249)),a=(e,t)=>{Object(i.a)(e,"show-dialog",{dialogTag:"dialog-box",dialogImport:s,dialogParams:t})},n=(e,t)=>{Object(i.a)(e,"show-dialog",{dialogTag:"dialog-box",dialogImport:s,dialogParams:Object.assign({},t,{confirmation:!0})})},o=(e,t)=>{Object(i.a)(e,"show-dialog",{dialogTag:"dialog-box",dialogImport:s,dialogParams:Object.assign({},t,{prompt:!0})})}},280:function(e,t,r){"use strict";r(108);var i=r(178);customElements.define("ha-icon-next",class extends i.a{connectedCallback(){super.connectedCallback(),setTimeout(()=>{this.icon="ltr"===window.getComputedStyle(this).direction?"hass:chevron-right":"hass:chevron-left"},100)}})},371:function(e,t,r){"use strict";var i=r(8),s=r(93);t.a=Object(i.a)(e=>(class extends e{navigate(...e){Object(s.a)(this,...e)}}))},387:function(e,t,r){"use strict";r.d(t,"a",function(){return s});var i=r(46);const s=(e,t)=>Object(i.a)(e,{message:t.localize("ui.common.successfully_saved")})},796:function(e,t,r){"use strict";r.r(t);r(269);var i=r(11),s=r(21),a=r(4),n=r(29),o=r(371),c=(r(142),r(184),r(239),r(280),r(177),r(256),r(176)),l=r(182),d=r(94),u=r(260);let p=!1;customElements.define("ha-config-user-picker",class extends(Object(l.a)(Object(o.a)(Object(c.a)(n.a)))){static get template(){return a.a`
      <style>
        ha-fab {
          position: fixed;
          bottom: 16px;
          right: 16px;
          z-index: 1;
        }
        ha-fab[is-wide] {
          bottom: 24px;
          right: 24px;
        }
        ha-fab[rtl] {
          right: auto;
          left: 16px;
        }
        ha-fab[narrow] {
          bottom: 84px;
        }
        ha-fab[rtl][is-wide] {
          bottom: 24px;
          right: auto;
          left: 24px;
        }

        ha-card {
          max-width: 600px;
          margin: 16px auto;
          overflow: hidden;
        }
        a {
          text-decoration: none;
          color: var(--primary-text-color);
        }
      </style>

      <hass-tabs-subpage
        hass="[[hass]]"
        narrow="[[narrow]]"
        route="[[route]]"
        back-path="/config"
        tabs="[[_computeTabs()]]"
      >
        <ha-card>
          <template is="dom-repeat" items="[[users]]" as="user">
            <a href="[[_computeUrl(user)]]">
              <paper-item>
                <paper-item-body two-line>
                  <div>[[_withDefault(user.name, 'Unnamed User')]]</div>
                  <div secondary="">
                    [[_computeGroup(localize, user)]]
                    <template is="dom-if" if="[[user.system_generated]]">
                      -
                      [[localize('ui.panel.config.users.picker.system_generated')]]
                    </template>
                  </div>
                </paper-item-body>
                <ha-icon-next></ha-icon-next>
              </paper-item>
            </a>
          </template>
        </ha-card>

        <ha-fab
          is-wide$="[[isWide]]"
          narrow$="[[narrow]]"
          icon="hass:plus"
          title="[[localize('ui.panel.config.users.picker.add_user')]]"
          on-click="_addUser"
          rtl$="[[rtl]]"
        ></ha-fab>
      </hass-tabs-subpage>
    `}static get properties(){return{hass:Object,users:Array,isWide:Boolean,narrow:Boolean,route:Object,rtl:{type:Boolean,reflectToAttribute:!0,computed:"_computeRTL(hass)"}}}connectedCallback(){super.connectedCallback(),p||(p=!0,this.fire("register-dialog",{dialogShowEvent:"show-add-user",dialogTag:"ha-dialog-add-user",dialogImport:()=>Promise.all([r.e(1),r.e(44)]).then(r.bind(null,770))}))}_withDefault(e,t){return e||t}_computeUrl(e){return`/config/users/${e.id}`}_computeGroup(e,t){return e(`groups.${t.group_ids[0]}`)}_computeRTL(e){return Object(d.a)(e)}_computeTabs(){return u.configSections.persons}_addUser(){this.fire("show-add-user",{hass:this.hass,dialogClosedCallback:async({userId:e})=>{this.fire("reload-users"),e&&this.navigate(`/config/users/${e}`)}})}});var h=r(0),f=r(704),m=(r(84),r(54)),b=r(14),g=r(93),y=r(449),v=r(387),w=r(197);function k(e){var t,r=E(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function _(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function j(e){return e.decorators&&e.decorators.length}function x(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function O(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function E(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}const $=[y.b,y.a];!function(e,t,r,i){var s=function(){var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach(function(r){t.forEach(function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)},this)},this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach(function(i){t.forEach(function(t){var s=t.placement;if(t.kind===i&&("static"===s||"prototype"===s)){var a="static"===s?e:r;this.defineClassElement(a,t)}},this)},this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],s={static:[],prototype:[],own:[]};if(e.forEach(function(e){this.addElementPlacement(e,s)},this),e.forEach(function(e){if(!j(e))return r.push(e);var t=this.decorateElement(e,s);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)},this),!t)return{elements:r,finishers:i};var a=this.decorateConstructor(r,t);return i.push.apply(i,a.finishers),a.finishers=i,a},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],s=e.decorators,a=s.length-1;a>=0;a--){var n=t[e.placement];n.splice(n.indexOf(e.key),1);var o=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,s[a])(o)||o);e=c.element,this.addElementPlacement(e,t),c.finisher&&i.push(c.finisher);var l=c.extras;if(l){for(var d=0;d<l.length;d++)this.addElementPlacement(l[d],t);r.push.apply(r,l)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var s=this.fromClassDescriptor(e),a=this.toClassDescriptor((0,t[i])(s)||s);if(void 0!==a.finisher&&r.push(a.finisher),void 0!==a.elements){e=a.elements;for(var n=0;n<e.length-1;n++)for(var o=n+1;o<e.length;o++)if(e[n].key===e[o].key&&e[n].placement===e[o].placement)throw new TypeError("Duplicated element ("+e[n].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if(Symbol.iterator in Object(e)||"[object Arguments]"===Object.prototype.toString.call(e))return Array.from(e)}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance")}()).map(function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t},this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=E(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var s=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var a={kind:t,key:r,placement:i,descriptor:Object.assign({},s)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(s,"get","The property descriptor of a field descriptor"),this.disallowProperty(s,"set","The property descriptor of a field descriptor"),this.disallowProperty(s,"value","The property descriptor of a field descriptor"),a.initializer=e.initializer),a},toElementFinisherExtras:function(e){var t=this.toElementDescriptor(e),r=O(e,"finisher"),i=this.toElementDescriptors(e.extras);return{element:t,finisher:r,extras:i}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=O(e,"finisher"),i=this.toElementDescriptors(e.elements);return{elements:i,finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}();if(i)for(var a=0;a<i.length;a++)s=i[a](s);var n=t(function(e){s.initializeInstanceElements(e,o.elements)},r),o=s.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===a.key&&e.placement===a.placement},i=0;i<e.length;i++){var s,a=e[i];if("method"===a.kind&&(s=t.find(r)))if(x(a.descriptor)||x(s.descriptor)){if(j(a)||j(s))throw new ReferenceError("Duplicated methods ("+a.key+") can't be decorated.");s.descriptor=a.descriptor}else{if(j(a)){if(j(s))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+a.key+").");s.decorators=a.decorators}_(a,s)}else t.push(a)}return t}(n.d.map(k)),e);s.initializeClassElements(n.F,o.elements),s.runClassFinishers(n.F,o.finishers)}([Object(h.d)("ha-user-editor")],function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[Object(h.g)()],key:"hass",value:void 0},{kind:"field",decorators:[Object(h.g)()],key:"user",value:void 0},{kind:"field",decorators:[Object(h.g)()],key:"narrow",value:void 0},{kind:"field",decorators:[Object(h.g)()],key:"route",value:void 0},{kind:"method",key:"render",value:function(){const e=this.hass,t=this.user;return e&&t?h.f`
      <hass-tabs-subpage
        .hass=${this.hass}
        .narrow=${this.narrow}
        .route=${this.route}
        .tabs=${u.configSections.persons}
      >
        <ha-card .header=${this._name}>
          <table class="card-content">
            <tr>
              <td>${e.localize("ui.panel.config.users.editor.id")}</td>
              <td>${t.id}</td>
            </tr>
            <tr>
              <td>${e.localize("ui.panel.config.users.editor.owner")}</td>
              <td>${t.is_owner}</td>
            </tr>
            <tr>
              <td>${e.localize("ui.panel.config.users.editor.group")}</td>
              <td>
                <select
                  @change=${this._handleGroupChange}
                  .value=${Object(f.a)(this.updateComplete.then(()=>t.group_ids[0]))}
                >
                  ${$.map(t=>h.f`
                      <option value=${t}>
                        ${e.localize(`groups.${t}`)}
                      </option>
                    `)}
                </select>
              </td>
            </tr>
            ${t.group_ids[0]===y.b?h.f`
                  <tr>
                    <td colspan="2" class="user-experiment">
                      The users group is a work in progress. The user will be
                      unable to administer the instance via the UI. We're still
                      auditing all management API endpoints to ensure that they
                      correctly limit access to administrators.
                    </td>
                  </tr>
                `:""}

            <tr>
              <td>${e.localize("ui.panel.config.users.editor.active")}</td>
              <td>${t.is_active}</td>
            </tr>
            <tr>
              <td>
                ${e.localize("ui.panel.config.users.editor.system_generated")}
              </td>
              <td>${t.system_generated}</td>
            </tr>
          </table>

          <div class="card-actions">
            <mwc-button @click=${this._handlePromptRenameUser}>
              ${e.localize("ui.panel.config.users.editor.rename_user")}
            </mwc-button>
            <mwc-button
              class="warning"
              @click=${this._promptDeleteUser}
              .disabled=${t.system_generated}
            >
              ${e.localize("ui.panel.config.users.editor.delete_user")}
            </mwc-button>
            ${t.system_generated?h.f`
                  ${e.localize("ui.panel.config.users.editor.system_generated_users_not_removable")}
                `:""}
          </div>
        </ha-card>
      </hass-tabs-subpage>
    `:h.f``}},{kind:"get",key:"_name",value:function(){return this.user&&(this.user.name||this.hass.localize("ui.panel.config.users.editor.unnamed_user"))}},{kind:"method",key:"_handleRenameUser",value:async function(e){if(null!==e&&e!==this.user.name)try{await Object(y.e)(this.hass,this.user.id,{name:e}),Object(b.a)(this,"reload-users")}catch(t){Object(w.a)(this,{text:`${this.hass.localize("ui.panel.config.users.editor.user_rename_failed")} ${t.message}`})}}},{kind:"method",key:"_handlePromptRenameUser",value:async function(e){e.currentTarget.blur(),Object(w.c)(this,{title:this.hass.localize("ui.panel.config.users.editor.enter_new_name"),defaultValue:this.user.name,inputLabel:this.hass.localize("ui.panel.config.users.add_user.name"),confirm:e=>this._handleRenameUser(e)})}},{kind:"method",key:"_handleGroupChange",value:async function(e){const t=e.currentTarget,r=t.value;try{await Object(y.e)(this.hass,this.user.id,{group_ids:[r]}),Object(v.a)(this,this.hass),Object(b.a)(this,"reload-users")}catch(i){Object(w.a)(this,{text:`${this.hass.localize("ui.panel.config.users.editor.group_update_failed")} ${i.message}`}),t.value=this.user.group_ids[0]}}},{kind:"method",key:"_deleteUser",value:async function(){try{await Object(y.c)(this.hass,this.user.id)}catch(e){return void Object(w.a)(this,{text:e.code})}Object(b.a)(this,"reload-users"),Object(g.a)(this,"/config/users")}},{kind:"method",key:"_promptDeleteUser",value:async function(e){Object(w.b)(this,{text:this.hass.localize("ui.panel.config.users.editor.confirm_user_deletion","name",this._name),confirm:()=>this._deleteUser()})}},{kind:"get",static:!0,key:"styles",value:function(){return[m.a,h.c`
        .card-actions {
          display: flex;
          justify-content: space-between;
          align-items: center;
        }
        ha-card {
          max-width: 600px;
          margin: 16px auto 16px;
        }
        hass-subpage ha-card:first-of-type {
          direction: ltr;
        }
        table {
          width: 100%;
        }
        td {
          vertical-align: top;
        }
        .user-experiment {
          padding: 8px 0;
        }
      `]}}]}},h.a);customElements.define("ha-config-users",class extends(Object(o.a)(n.a)){static get template(){return a.a`
      <app-route
        route="[[route]]"
        pattern="/:user"
        data="{{_routeData}}"
      ></app-route>

      <template is="dom-if" if='[[_equals(_routeData.user, "picker")]]'>
        <ha-config-user-picker
          hass="[[hass]]"
          users="[[_users]]"
          is-wide="[[isWide]]"
          narrow="[[narrow]]"
          route="[[route]]"
        ></ha-config-user-picker>
      </template>
      <template
        is="dom-if"
        if='[[!_equals(_routeData.user, "picker")]]'
        restamp
      >
        <ha-user-editor
          hass="[[hass]]"
          user="[[_computeUser(_users, _routeData.user)]]"
          narrow="[[narrow]]"
          route="[[route]]"
        ></ha-user-editor>
      </template>
    `}static get properties(){return{hass:Object,isWide:Boolean,narrow:Boolean,route:{type:Object,observer:"_checkRoute"},_routeData:Object,_user:{type:Object,value:null},_users:{type:Array,value:null}}}ready(){super.ready(),this._loadData(),this.addEventListener("reload-users",()=>this._loadData())}_handlePickUser(e){this._user=e.detail.user}_checkRoute(e){Object(b.a)(this,"iron-resize"),this._debouncer=s.a.debounce(this._debouncer,i.d.after(0),()=>{""===e.path&&this.navigate(`${e.prefix}/picker`,!0)})}_computeUser(e,t){return e&&e.filter(e=>e.id===t)[0]}_equals(e,t){return e===t}async _loadData(){this._users=await Object(y.d)(this.hass)}})}}]);
//# sourceMappingURL=chunk.d497ec89128ec4f9ec48.js.map