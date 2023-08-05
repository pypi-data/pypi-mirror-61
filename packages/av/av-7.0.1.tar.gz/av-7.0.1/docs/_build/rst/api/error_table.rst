============================  ===============================  ============================================================
Exception Class               Code/Enum Name                   FFmpeg Error Message                                        
============================  ===============================  ============================================================
``av.BSFNotFoundError``       ``av.error.BSF_NOT_FOUND``       Bitstream filter not found                                  
``av.BugError``               ``av.error.BUG``                 Internal bug, should not have happened                      
``av.BufferTooSmallError``    ``av.error.BUFFER_TOO_SMALL``    Buffer too small                                            
``av.DecoderNotFoundError``   ``av.error.DECODER_NOT_FOUND``   Decoder not found                                           
``av.DemuxerNotFoundError``   ``av.error.DEMUXER_NOT_FOUND``   Demuxer not found                                           
``av.EncoderNotFoundError``   ``av.error.ENCODER_NOT_FOUND``   Encoder not found                                           
``av.EOFError``               ``av.error.EOF``                 End of file                                                 
``av.ExitError``              ``av.error.EXIT``                Immediate exit requested                                    
``av.ExternalError``          ``av.error.EXTERNAL``            Generic error in an external library                        
``av.FilterNotFoundError``    ``av.error.FILTER_NOT_FOUND``    Filter not found                                            
``av.InvalidDataError``       ``av.error.INVALIDDATA``         Invalid data found when processing input                    
``av.MuxerNotFoundError``     ``av.error.MUXER_NOT_FOUND``     Muxer not found                                             
``av.OptionNotFoundError``    ``av.error.OPTION_NOT_FOUND``    Option not found                                            
``av.PatchWelcomeError``      ``av.error.PATCHWELCOME``        Not yet implemented in FFmpeg, patches welcome              
``av.ProtocolNotFoundError``  ``av.error.PROTOCOL_NOT_FOUND``  Protocol not found                                          
``av.UnknownError``           ``av.error.UNKNOWN``             Unknown error occurred                                      
``av.ExperimentalError``      ``av.error.EXPERIMENTAL``        Experimental feature                                        
``av.InputChangedError``      ``av.error.INPUT_CHANGED``       Input changed                                               
``av.OutputChangedError``     ``av.error.OUTPUT_CHANGED``      Output changed                                              
``av.HTTPBadRequestError``    ``av.error.HTTP_BAD_REQUEST``    Server returned 400 Bad Request                             
``av.HTTPUnauthorizedError``  ``av.error.HTTP_UNAUTHORIZED``   Server returned 401 Unauthorized (authorization failed)     
``av.HTTPForbiddenError``     ``av.error.HTTP_FORBIDDEN``      Server returned 403 Forbidden (access denied)               
``av.HTTPNotFoundError``      ``av.error.HTTP_NOT_FOUND``      Server returned 404 Not Found                               
``av.HTTPOtherClientError``   ``av.error.HTTP_OTHER_4XX``      Server returned 4XX Client Error, but not one of 40{0,1,3,4}
``av.HTTPServerError``        ``av.error.HTTP_SERVER_ERROR``   Server returned 5XX Server Error reply                      
============================  ===============================  ============================================================
