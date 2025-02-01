// This is a sample code for adding two numbers
module add (
    input  wire  [31:0]  a         ,
    input  wire  [31:0]  b         ,
    output wire [31:0]   sum       ,
    output logic         overflow
) ;

always @(*) begin 
    {overflow, sum} = a + b;
end
endmodule

//  module add (
// input   [31:0]  a        ,
// input   [31:0]  b        ,
// output  [31:0]  sum      ,
// output         overflow );