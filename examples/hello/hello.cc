/// @file
///
/// This Example shows how to compile and run drake files
#indlue <gflags/gflags.h>
#include "drake/common/text_logging_gflags.h"

namespace drake{
namespace examples{
namespace hello{


DEFINE_string(your_name, "Anirudh",
            "Putting your name here so Drake recognizes you."
);


}
}
}