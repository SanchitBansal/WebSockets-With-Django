$(function() {
      function guid() {
                  function s4() {
                    return Math.floor((1 + Math.random()) * 0x10000)
                      .toString(16)
                      .substring(1);
                  }
                  return s4() + s4() + '-' + s4() + '-' + s4() + '-' +
                    s4() + '-' + s4() + s4() + s4();
                }
      var uid = guid();

      var connection = new WebSocket('{{ WebsocketsURL }}?id=' + uid + '&path={{ logfile }}.txt');
      connection.onopen = function () {
              console.log('Ping'); // Send the message 'Ping' to the server
          };
      connection.onerror = function (error) {
              $(".progress-bar-row").hide();
              $('#logbox').html("Socket Connection Error. Worry not, only logs are not viewable, rest everything is normal.");
              connection.onclose = function () {}; // disable onclose handler first
              connection.close()
              console.log('WebSocket Error ' + error);
          };
          
      // Log messages from the server
      connection.onmessage = function (e) {
                  content = nl2br(e.data);
                  if(content == "--BLANK--") {
                          $('#logbox').html("Hold on... Logs are coming through, just give it a few seconds.");
                  }
                  else {
                          $('#logbox').append(content);
                          if(content.indexOf("---- END OF LOGS ----") != -1) {
                                connection.onclose = function () {}; // disable onclose handler first
                                connection.close()
                          }
                        }
                  //console.log('Server: ' + e.data);
                };

      window.onbeforeunload = function() {
                connection.onclose = function () {}; // disable onclose handler first
                connection.close()
            };
            
      function nl2br (str, is_xhtml) {
                        var breakTag = (is_xhtml || typeof is_xhtml === 'undefined') ? '<br />' : '<br>';
                        return (str + '').replace(/([^>\r\n]?)(\r\n|\n\r|\r|\n)/g, '$1' + breakTag + '$2');
                        }
        });


