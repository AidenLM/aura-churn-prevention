export default function CalculatorLoading() {
  return (
    <div className="min-h-screen bg-[#F4F5F7]">
      {/* Header Skeleton */}
      <header className="border-b border-gray-200 bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-8 py-5">
          <div className="w-48 h-8 bg-gray-200 rounded animate-pulse mb-2"></div>
          <div className="w-64 h-4 bg-gray-100 rounded animate-pulse"></div>
        </div>
      </header>

      {/* Main Content Skeleton */}
      <main className="max-w-7xl mx-auto px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Form Skeleton - Left Side */}
          <div className="lg:col-span-2 space-y-6">
            {/* Profile Section */}
            <div className="bg-white rounded-lg border border-gray-200 p-8 shadow-sm">
              <div className="w-40 h-6 bg-gray-200 rounded animate-pulse mb-6"></div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {[1, 2, 3, 4].map((i) => (
                  <div key={i}>
                    <div className="w-32 h-4 bg-gray-200 rounded animate-pulse mb-2"></div>
                    <div className="w-full h-10 bg-gray-100 rounded-lg animate-pulse"></div>
                  </div>
                ))}
              </div>
            </div>

            {/* Usage Section */}
            <div className="bg-white rounded-lg border border-gray-200 p-8 shadow-sm">
              <div className="w-40 h-6 bg-gray-200 rounded animate-pulse mb-6"></div>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {[1, 2, 3].map((i) => (
                  <div key={i}>
                    <div className="w-32 h-4 bg-gray-200 rounded animate-pulse mb-2"></div>
                    <div className="w-full h-10 bg-gray-100 rounded-lg animate-pulse"></div>
                  </div>
                ))}
              </div>
            </div>

            {/* Risk Indicators Section */}
            <div className="bg-white rounded-lg border border-gray-200 p-8 shadow-sm">
              <div className="w-40 h-6 bg-gray-200 rounded animate-pulse mb-6"></div>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {[1, 2, 3].map((i) => (
                  <div key={i}>
                    <div className="w-32 h-4 bg-gray-200 rounded animate-pulse mb-2"></div>
                    <div className="w-full h-10 bg-gray-100 rounded-lg animate-pulse"></div>
                  </div>
                ))}
              </div>
            </div>

            {/* Button Skeleton */}
            <div className="w-full h-14 bg-gray-200 rounded-lg animate-pulse"></div>
          </div>

          {/* Results Skeleton - Right Side */}
          <div className="space-y-6">
            <div className="bg-white rounded-lg border border-gray-200 p-8 shadow-sm">
              <div className="w-32 h-32 bg-gray-200 rounded-full mx-auto animate-pulse mb-4"></div>
              <div className="w-24 h-6 bg-gray-200 rounded mx-auto animate-pulse"></div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
